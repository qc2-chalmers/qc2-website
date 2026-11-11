#!/usr/bin/env python3
"""Mirror the calibration toolkit documentation into the website build.

The docs are a static Sphinx build hosted elsewhere. This script copies every
page and asset into ``toolkit-docs/`` so the website serves them from its own
domain. Assets the docs pull from sibling paths on the same host (e.g. the
interactive Bloch-sphere widget) are copied into ``toolkit-docs/_ext/`` and every
reference to the source host is rewritten, so the original address never
appears on the published site.

It runs as the Vercel build command (see vercel.json) on every deployment, so the
copy is never committed. Only the Python standard library is used, so it also
runs locally for testing:

    python3 scripts/sync_docs.py
    python3 -m http.server   # then open http://localhost:8000/docs.html

The source URL is DOCS_SOURCE_URL below (an environment variable of the same
name overrides it). It never appears on the published site.
If it can't be fetched the build fails and Vercel keeps the previous deployment.
"""

import os
import posixpath
import re
import shutil
import sys
import tempfile
import urllib.parse
import urllib.request
from collections import deque
from html.parser import HTMLParser
from pathlib import Path

# Where the GitLab CI publishes the built docs (overridable via the env var).
DOCS_SOURCE_URL = "https://webfiles.portal.chalmers.se/qt-white/autocalibration_docs/"

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_NAME = "toolkit-docs"
OUT_DIR = REPO_ROOT / OUT_NAME
# Path the mirror is served from on the website. JavaScript resolves relative
# URLs against the *page*, not the script, so JS files get site-absolute paths.
SITE_PATH = f"/{OUT_NAME}/"
TEXT_EXT = {".html", ".css", ".js", ".txt", ".json", ".xml"}
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")
CSS_IMPORT = re.compile(r"@import\s+['\"]([^'\"]+)['\"]")


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value and name in ("href", "src", "data-src", "poster"):
                self.links.append(value)
            elif value and name == "srcset":
                self.links += [p.strip().split(" ")[0] for p in value.split(",")]
            elif value and name == "style":
                self.links += CSS_URL.findall(value)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "docs-mirror"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


class Mirror:
    def __init__(self, base):
        self.base = base if base.endswith("/") else base + "/"
        parsed = urllib.parse.urlparse(self.base)
        self.origin = f"{parsed.scheme}://{parsed.netloc}"
        self.docs_path = parsed.path                                   # /a/b/docs/
        self.root_path = posixpath.dirname(self.docs_path.rstrip("/")) + "/"  # /a/b/
        self.root = self.origin + self.root_path
        # Full URLs or host-absolute paths under the shared root.
        self.abs_ref = re.compile(
            r"(?:" + re.escape(self.origin) + r")?" + re.escape(self.root_path) + r"[^\s'\"()<>`]*"
        )

    def in_scope(self, url):
        return url.startswith(self.root)

    def local(self, url):
        """Local path (relative to the mirror root) for an in-scope URL."""
        path = urllib.parse.urlparse(url).path
        if path.startswith(self.docs_path):
            rel = path[len(self.docs_path):]
        else:
            rel = "_ext/" + path[len(self.root_path):]
        return urllib.parse.unquote(rel)

    def file_for(self, url):
        rel = self.local(url)
        return rel + "index.html" if rel == "" or rel.endswith("/") else rel

    def rewrite(self, text, file_rel):
        is_js = file_rel.endswith(".js")
        file_dir = posixpath.dirname(file_rel)

        def sub(m):
            ref = m.group(0)
            url = urllib.parse.urljoin(self.origin, ref)
            split = urllib.parse.urlsplit(url)
            target = self.local(urllib.parse.urlunsplit(split._replace(query="", fragment="")))
            if is_js:
                new = SITE_PATH + target
            else:
                new = posixpath.relpath(target or ".", file_dir or ".")
                if target == "" or target.endswith("/"):
                    new = new.rstrip("/") + "/"
                if not new.startswith("."):
                    new = "./" + new  # ES module imports reject bare specifiers
            if split.query:
                new += "?" + split.query
            if split.fragment:
                new += "#" + split.fragment
            return new

        return self.abs_ref.sub(sub, text)

    def run(self, tmp):
        seen, failures = set(), []
        queue = deque([self.base, self.base + "searchindex.js", self.base + "objects.inv"])
        while queue:
            url = urllib.parse.urldefrag(queue.popleft())[0].split("?")[0]
            if url in seen or not self.in_scope(url):
                continue
            seen.add(url)
            try:
                data = fetch(url)
            except Exception as exc:  # a broken link in the docs should not abort the sync
                failures.append(f"{self.local(url) or 'index'}: {exc}")
                continue

            rel = self.file_for(url)
            target = tmp / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

            suffix = target.suffix.lower()
            if suffix not in TEXT_EXT:
                continue
            text = data.decode("utf-8", errors="replace")
            links = [m.group(0) for m in self.abs_ref.finditer(text)]
            if suffix == ".html":
                parser = LinkParser()
                parser.feed(text)
                links += parser.links
            elif suffix == ".css":
                links += CSS_URL.findall(text) + CSS_IMPORT.findall(text)
            for link in links:
                if link.startswith(("data:", "mailto:", "javascript:", "#")):
                    continue
                queue.append(urllib.parse.urljoin(url, link))

        for f in tmp.rglob("*"):
            if f.is_file() and f.suffix.lower() in TEXT_EXT:
                text = f.read_text(encoding="utf-8", errors="replace")
                new = self.rewrite(text, f.relative_to(tmp).as_posix())
                if new != text:
                    f.write_text(new, encoding="utf-8")
        return len(seen) - len(failures), failures


def main():
    base = os.environ.get("DOCS_SOURCE_URL", "").strip() or DOCS_SOURCE_URL

    mirror = Mirror(base)
    tmp = Path(tempfile.mkdtemp())
    count, failures = mirror.run(tmp)

    if not (tmp / "index.html").exists():
        sys.exit("Mirror failed: index.html was not downloaded")
    leaks = [str(f.relative_to(tmp)) for f in tmp.rglob("*") if f.is_file()
             and urllib.parse.urlparse(mirror.base).netloc.encode() in f.read_bytes()]
    if leaks:
        sys.exit("Mirror failed: source host still referenced in " + ", ".join(leaks))

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    shutil.move(str(tmp), OUT_DIR)
    print(f"Mirrored {count} files into {OUT_NAME}/")
    for line in failures:
        print("  skipped", line)


if __name__ == "__main__":
    main()
