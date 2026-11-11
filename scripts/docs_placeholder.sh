#!/bin/sh
# Fallback used by the Vercel build when the toolkit docs could not be mirrored
# (python3 missing, docs server unreachable, ...). The site still deploys and
# the docs link shows a friendly page instead of a 404.
mkdir -p toolkit-docs
cat > toolkit-docs/index.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>QC2 · Documentation</title>
  <style>
    body { margin: 0; min-height: 100vh; display: grid; place-items: center; font-family: system-ui, sans-serif;
           background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); color: #0f172a; }
    main { max-width: 32rem; margin: 1rem; padding: 2.5rem; text-align: center; background: #fff;
           border-radius: 1.5rem; box-shadow: 0 20px 40px -20px rgba(15, 23, 42, .3); }
    a { display: inline-block; margin-top: 1rem; padding: .7rem 1.2rem; border-radius: 999px; color: #fff;
        text-decoration: none; font-weight: 600; background: linear-gradient(120deg, #3b82f6, #6366f1, #8b5cf6); }
  </style>
</head>
<body>
  <main>
    <h1>📖 Documentation coming back soon</h1>
    <p>The calibration toolkit documentation is being updated. Please check again in a little while.</p>
    <a href="../software.html">← Back to Software</a>
  </main>
</body>
</html>
HTML
echo "Toolkit docs not mirrored: placeholder page written to toolkit-docs/index.html"
