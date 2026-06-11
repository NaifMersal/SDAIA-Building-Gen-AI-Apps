# AI Agents — Project Starter

Build a production-grade multi-agent research system from scratch.
You are given the observability foundation and a working `BaseAgent` skeleton.
Your job: implement the ReAct loop, then design your own multi-agent pipeline.

---

## Structure

```
project_starter/
├── pyproject.toml           # Dependencies
├── .env.example             # Environment variable template
└── src/
    ├── config.py            # Pydantic settings (complete)
    ├── exceptions.py        # Custom exceptions (complete)
    ├── logger.py            # Structured logging (complete)
    ├── main.py              # Typer CLI (TODO: wire OrchestratorAgent)
    ├── agent/
    │   ├── base.py          # BaseAgent — skeleton (TODO: ReAct loop)
    │   ├── orchestration.py # OrchestratorAgent — entirely TODO (your design)
    │   └── prompts.py       # System prompts — entirely TODO (your design)
    ├── observability/
    │   ├── observe.py       # @observe decorator & langfuse_context stub (complete)
    │   └── loop_detector.py # LoopDetector (complete)
    └── tools/
        ├── registry.py      # ToolRegistry (complete)
        └── search_tool.py   # search_web + read_webpage (complete)
```

---

## Setup

```bash
# 1. Install dependencies
uv pip install -e .

# 2. Configure secrets
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY (or another provider key)

# 3. Verify the foundation
uv run python tests/verify_components.py
```

---

### Step 1 — `src/agent/base.py` → `BaseAgent.run()`
Implement the ReAct loop. You are provided with the observability logic (`@observe`), a `LoopDetector`, and a tool execution helper (`_execute_tool`). You must build the core loop that handles the conversation history and tool-calling logic.

### Step 2 — `src/agent/prompts.py`
Perform prompt engineering to define the roles and standards for your specialized agents (Researcher, Analyst, Writer, etc.).

### Step 3 — `src/agent/orchestration.py` → `OrchestratorAgent`
Design and implement your own multi-agent pipeline. You will instantiate multiple `BaseAgent` objects with different prompts and tools, then coordinate them.

| Strategy | Description |
|---|---|
| Sequential chain | Researcher → Analyst → Writer |
| Retry loop | Re-research if confidence is low |
| Planner-first | Planner breaks query → specialists execute |
| Your own idea | Surprise us! |

**Teaches**: multi-agent design, orchestration patterns, complex async workflows.

---

### Step 3 — `src/main.py` → `research()`
Wire your `OrchestratorAgent` into the Typer CLI so it can be called from the terminal.

**Verify**: `uv run python -m src.main --query "Compare LLMs"` produces a full report.

---

## Quick Reference

```bash
uv pip install -e .                   # install dependencies
uv run python tests/verify_components.py # verify components
uv run python -m src.main "..."       # run query
```
