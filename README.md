<img src="images/qc2_logo_dark.png" alt="QC2 Lab Logo" width="200">

Welcome to the official webpage of the **QC2 LAB** based at Chalmers University of Technology. 

## About the Group
Supported by the Wallenberg foundations and situated within the Chalmers Microtechnology and Nanoscience department, our group focuses on developing a scalable 100-qubit superconducting quantum processor. We bridge the gap between academic theoretical research and industrial hardware engineering to foster a robust ecosystem for quantum technology.

## How It's Built
This website is built using a modern, responsive web stack designed for performance and accessibility:

* **Framework**: Built with **Bootstrap 5**, providing a mobile-first, responsive grid system and pre-styled UI components.
* **Styling**: Custom CSS managed through a theme-aware architecture, supporting both **Light and Dark modes** via `data-bs-theme`.
* **Icons**: Uses inline **SVG symbols** for fast, high-resolution iconography without external dependencies.
* **Interactivity**: 
    * **Carousel**: A custom-configured Bootstrap carousel for showcasing laboratory and research images.
    * **Theme Switching**: A self-contained JavaScript module (`color-modes.js`) that handles user theme preferences and storage.
    * **Content Rendering**: Modular layout using consistent "content blocks" to ensure a unified look across the Home, People, and Publications pages.

## Project Structure
- `/css`: Contains Bootstrap framework files and custom style overrides.
- `/images`: Organized by category (`carousel/`, `people/`, `papers/`, `blog/`) for easy management.
- `/js`: Contains standard Bootstrap scripts and custom theme-switching logic.
- `index.html`: The main landing page.
- `people.html`: Team member profiles and professional information.
- `publications.html`: Archived research papers and experimental studies.

## Getting Started
To view the website locally, simply open the `index.html` file in any modern web browser. No compilation or build steps are required.