# Everything-ML Documentation

This repository contains the source code for the "Everything-ML" documentation website, built with [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. It is designed to replicate a clean, professional documentation style similar to OpenAI's platform.

## Prerequisites

- **Python**: Ensure you have Python 3.x installed.
- **pip**: Python package installer.

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/nishchalnishant/Everything-ML.git
    cd Everything-ML
    ```

2.  **Install MkDocs and the Material Theme**:
    ```bash
    pip install mkdocs mkdocs-material
    ```

## Usage

### Local Development

To serve the website locally and preview changes in real-time:

```bash
mkdocs serve
```

Open your browser and navigate to `http://127.0.0.1:8000/`.

### Building the Static Site

To build the static HTML files (output to the `site/` directory):

```bash
mkdocs build
```

## Deployment to GitHub Pages

This project is configured to easily deploy to GitHub Pages.

1.  **One-command deployment**:
    ```bash
    mkdocs gh-deploy
    ```

    This command builds the documentation and pushes it to the `gh-pages` branch of your repository.

2.  **GitHub Settings**:
    - Go to your repository on GitHub.
    - Navigate to **Settings** > **Pages**.
    - Ensure the **Source** is set to `Deploy from a branch` and select `gh-pages` / `root`.

## Project Structure

```text
Everything-ML/
├── mkdocs.yml              # Main configuration file
├── docs/                   # Documentation source files
│   ├── index.md
│   ├── supervised/
│   ├── unsupervised/
│   └── deep-learning/
└── stylesheets/            # Custom CSS customization
```
