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
    ├── utils.py             # Helpers (complete)
    ├── agent/
    │   ├── base.py          # BaseAgent — __init__ + hooks complete; run() is TODO
    │   ├── orchestration.py # OrchestratorAgent — entirely TODO (your design)
    │   └── prompts.py       # System prompts for example roles you can use, or add your own
    ├── observability/
    │   ├── tracer.py        # AgentTracer, AgentStep, ToolCallRecord (complete)
    │   ├── loop_detector.py # AdvancedLoopDetector (complete)
    │   └── cost_tracker.py  # CostTracker (TODO: log_completion, print_cost_breakdown)
    └── tools/
        ├── registry.py      # ToolRegistry (TODO: register, get_tool, …)
        └── search_tool.py   # search_web + read_webpage (complete)
```

---

## Setup

```bash
# 1. Install dependencies
uv pip install -e .

# 2. Configure secrets
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY (or another provider key)

# 3. Verify your environment before you start coding
uv run python tests/verify_components.py
```

---

## Student Build Order

Work through the TODOs in this order — each step unlocks the next.

### Step 1 — `src/tools/registry.py`
Implement `register()`, `get_tool()`, `get_all_tools()`,
`get_tools_by_category()`, and `execute_tool()`.

**Teaches**: decorator pattern, registry pattern.
**Verify**: `uv run python tests/verify_components.py` → `test_registry` passes.

---

### Step 2 — `src/observability/cost_tracker.py`
Implement `log_completion()` and `print_cost_breakdown()`.

**Teaches**: token extraction from LiteLLM responses, cost APIs.
**Verify**: `uv run python tests/verify_components.py` → all 3 tests pass.

---

### Step 3 — `src/agent/base.py` → `run()`
Implement the ReAct loop. The docstring in `run()` gives you step-by-step
guidance. Key requirements:
- Use `acompletion()` from LiteLLM for each step
- Execute ALL tool calls **in parallel** with `asyncio.gather()`
- Call the provided hook methods (`_on_step_start`, `_on_step_end`, `_on_loop_end`)
- Handle errors gracefully

**Teaches**: ReAct pattern, async parallel execution, observability hooks.
**Verify**: `uv run python -m src.main "What is RAG?"` runs end-to-end (after Step 1).

---

### Step 4 — `src/agent/orchestration.py` → `OrchestratorAgent`
Design and implement your own multi-agent pipeline. There is no single
correct answer — pick a strategy that interests you:

| Strategy | Description |
|---|---|
| Sequential chain | Researcher → Analyst → Writer |
| Parallel + synthesize | Researcher ∥ Fact-checker → Writer |
| Retry loop | Re-research if confidence is low |
| Planner-first | Planner breaks query → specialists execute |
| Your own idea | Surprise us! |

**Teaches**: multi-agent design, orchestration patterns.

---

### Step 5 — `src/main.py` → `research()`
Wire `OrchestratorAgent` into the Typer CLI.

**Verify**: `uv run python -m src.main --query "Compare LLMs"` produces a full report.

---

## Quick Reference

```bash
uv pip install -e .                   # install dependencies
uv run python tests/verify_components.py # verify components
uv run python -m src.main "..."       # run query
```

Available prompts in `src/agent/prompts.py`:
- `DEFAULT_SYSTEM_PROMPT`
- `RESEARCHER_PROMPT`
- `ANALYST_PROMPT`
- `WRITER_PROMPT`
- `FACT_CHECKER_PROMPT`
- `PLANNER_PROMPT`
