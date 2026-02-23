# Lab 00: Initialize `uv`

This lab guides you through installing and initializing `uv`, a fast Python package manager and resolver.

## 1. Install `uv`

### Windows (PowerShell)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2. Initialize Project

Navigate to your project directory and run:

```bash
uv init
```
This creates a `pyproject.toml` file.


## 3. Sync Dependencies

Install the dependencies specified in `pyproject.toml`:

```bash
uv sync
```

## 4. Using `uv pip` interface

`uv` provides a `pip`-compatible interface for lower-level package management.

### Create Virtual Environment

Create a virtual environment using Python 3.11:
```bash
uv venv -p 3.11
```

### Install a package manually
```bash
uv pip install requests
```

### List installed packages
```bash
uv pip list
```

### View requirements
```bash
uv pip freeze
```
