# Lab 00: Initialize `uv`

This lab guides you through installing and using `uv`, a fast Python package manager and resolver.

## 1. Install `uv`

### Windows (PowerShell)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2. Create Virtual Environment

The primary way we will use `uv` is to manage virtual environments and install packages using its `pip`-compatible interface.

### Create the Environment
Create a virtual environment using Python 3.11:
```bash
uv venv -p 3.11
```

## 3. Install Packages

You can install packages directly into the virtual environment using `uv pip`. This is just like `pip`, but much faster!

```bash
uv pip install requests
```

### Manage Packages
```bash
# List installed packages
uv pip list

# View requirements
uv pip freeze
```

---

## 4. Running Your Code

Once you have your environment set up and packages installed, there are two ways to run your Python scripts.

### Method A: Using `uv run` (Modern)
This is the easiest way. You don't need to manually "activate" anything. `uv` will automatically find the virtual environment in your current folder and run the script inside it.

```bash
uv run main.py
```

### Method B: Manual Activation (Traditional)
If you prefer the traditional way (where your terminal prompt shows the environment name), you can activate it manually:

**Windows:**
```powershell
.\.venv\Scripts\activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

Then you can run your script using `python`:
```bash
python main.py
```

---

## 5. Bonus: Advanced Project Management

`uv` also offers a "Project" mode that automates environment management and dependency tracking.

### Initialize a Project
Navigate to your project directory and run:
```bash
uv init
```

### Why use `uv init`?
This command creates several important files that define your development environment:
- **`pyproject.toml`**: The standard configuration file for Python projects. It lists your project's metadata and dependencies.
- **`.python-version`**: Tells `uv` (and other tools) which Python version to use for this project.
- **`main.py`**: A sample script to get you started.
- **`README.md`**: A basic project description file.

### Reproducibility with `uv.lock`
When you add a dependency (e.g., `uv add requests`), `uv` creates a `uv.lock` file. This file records the **exact** version of every package installed. This ensures that your code runs exactly the same way for everyone else.

### Ephemeral Tools with `uvx`
If you want to run a tool (like a linter or formatter) without installing it into your project, you can use `uvx`:
```bash
uvx ruff check .
```

