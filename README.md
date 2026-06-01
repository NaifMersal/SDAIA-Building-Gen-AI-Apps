# Gen-AI Engineering Lab — Course Materials

Welcome! This repository contains all lab exercises and homework for the course, along with the rendered slide decks hosted via GitHub Pages.

## Course Index & Slides

Browse all sessions and open any slide deck directly in your browser:

**[https://naifmersal.github.io/SDAIA-Building-Gen-AI-Apps/](https://naifmersal.github.io/SDAIA-Building-Gen-AI-Apps/)**

The index page lists every module's slides and links to the lab notebooks on GitHub.

### Slides offline

This branch contains the labs only. The rendered slide decks live on the
`gh-pages` branch. To grab them for offline use:

```bash
# Fresh, slides-only clone
git clone -b gh-pages --single-branch https://github.com/NaifMersal/SDAIA-Building-Gen-AI-Apps.git slides

# …or, from an existing clone of this repo
git fetch origin gh-pages
git worktree add ../slides gh-pages
```

Then open `slides/index.html` in your browser.

### Capstone Project

The capstone project starter code lives on a dedicated `project` branch. To access the project files, you can clone the branch directly or work from your existing clone:

```bash
# Fresh, project-only clone
git clone -b project --single-branch https://github.com/NaifMersal/SDAIA-Building-Gen-AI-Apps.git project

# ...or, from your existing clone, switch to the project branch directly:
git checkout project

# ...or, checkout the project branch into a separate sibling folder:
git fetch origin project
git worktree add ../project project
```

## Getting Started

### 1. Fork this Repository
Click **Fork** in the top-right corner to create your own copy. This lets you push your work without touching the original.

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 3. Set Up Your Environment
Each module's `labs/` folder contains a notebook with setup instructions. Generally:
```bash
pip install -r requirements.txt   # or follow the notebook's install cell
```

## Directory Structure

```
.
├── NN_module_name/
│   ├── labs/                      # Lab notebooks (fill in the TODOs)
│   └── homework/                  # Homework assignments
└── shared/                        # Shared helpers imported by labs
```

> Rendered slides are not on this branch — browse them at the [Course
> Index & Slides](#course-index--slides) link above, or clone the
> `gh-pages` branch (see *Slides offline*). The capstone project
> starter code is also hosted on a separate `project` branch (see *Capstone Project*).

## Working on Labs

- Open the `.ipynb` file in JupyterLab, VS Code, or Google Colab
- Fill in sections marked `# TODO`
- Run all cells top-to-bottom to verify your work

Happy learning!
