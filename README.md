<img src="images/qc2_logos/qc2_logo_dark.png" alt="QC2 Lab Logo" width="200">

Welcome to the official webpage of the **QC2 LAB** based at Chalmers University of Technology. 

## About the Group
Supported by the Wallenberg foundations and situated within the Chalmers Microtechnology and Nanoscience department (MC2), our group focuses on developing a scalable 100-qubit superconducting quantum processor. 

## How It's Built
This website is built using a modern, responsive web stack designed for performance and accessibility:

* **Framework**: Built with **Bootstrap 5**, providing a mobile-first, responsive grid system and pre-styled UI components.
* **Styling**: Custom CSS managed through a theme-aware architecture, supporting both **Light and Dark modes** via `data-bs-theme`.
* **Icons**: Uses inline **SVG symbols** for fast, high-resolution iconography without external dependencies.

## Project Structure
- `/css`: Contains Bootstrap framework files and custom style overrides.
- `/images`: Organized by category (`carousel/`, `people/`, `papers/`, `blog/`) for easy management.
- `/js`: Contains standard Bootstrap scripts and custom theme-switching logic.
- `/pages`: The source of every page (`index.html`, `people.html`, `publications.html`, `blog.html`, ...). **Edit pages here.**
- `/partials`: Blocks shared by all pages: `header.html` (navigation bar) and `footer.html` ("Supported by" logos).
- `/scripts/build_pages.py`: Builds the final pages in the site root from `pages/` + `partials/`.

## Getting Started
The navigation bar and footer live in one place (`partials/`), and each page in `pages/` contains a marker where they go:

```html
<!-- include: header -->                    <!-- navigation bar -->
<!-- include: header active=blog.html -->   <!-- ...with "News" highlighted (for sub-pages) -->
<!-- include: footer -->                    <!-- footer -->
```

To view the website locally, build the pages and serve the folder:

```sh
uv run scripts/build_pages.py     # or: python3 scripts/build_pages.py
python3 -m http.server            # then open http://localhost:8000
```

The generated pages in the site root are not committed (they are in `.gitignore`) — do not edit them, edit `pages/` instead and rebuild. Vercel runs the build on every deployment (see `vercel.json`).

To add a new page, copy an existing file in `pages/` (e.g. `pages/internship.html`), keep the include markers and replace the `<main>` content.