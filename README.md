# Gen-AI Engineering Lab — Course Materials

Welcome! This repository contains all lab exercises and homework for the course, along with the rendered slide decks hosted via GitHub Pages.

## Course Index & Slides

Browse all sessions and open any slide deck directly in your browser:

**[https://naifmersal.github.io/SDAIA-Building-Gen-AI-Apps/](https://naifmersal.github.io/SDAIA-Building-Gen-AI-Apps/)**

The index page lists every module's slides and links to the lab notebooks on GitHub.

## Getting Started

### 1. Fork this Repository
Click **Fork** in the top-right corner to create your own copy. This lets you push your work without touching the original.

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/Building-Gen-AI-Apps-students.git
cd Building-Gen-AI-Apps-students
```

### 3. Set Up Your Environment
Each module's `lab/` folder contains a notebook with setup instructions. Generally:
```bash
pip install -r requirements.txt   # or follow the notebook's install cell
```

## Directory Structure

```
.
├── docs/                          # Rendered slides (GitHub Pages)
│   ├── index.html                 # Course landing page
│   └── NN_module_name/slides/     # HTML slide decks per module
├── NN_module_name/
│   ├── lab/                       # Lab notebooks (fill in the TODOs)
│   └── homework/                  # Homework assignments
└── project_starter/               # Capstone project scaffold
```

## Working on Labs

- Open the `.ipynb` file in JupyterLab, VS Code, or Google Colab
- Fill in sections marked `# TODO`
- Run all cells top-to-bottom to verify your work

Happy learning!
