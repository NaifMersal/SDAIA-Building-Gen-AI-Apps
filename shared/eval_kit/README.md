# `eval_kit` — Shared evaluation primitives

A thin, growing artifact that threads through Modules 01 → 02b → 03 so
students see the same eval surface mature across the curriculum instead of
re-learning it three times.

## What's in here

| File | Purpose |
|---|---|
| `judge.py` | `LLMJudge` + `JudgeVerdict` — one-rubric LLM-as-judge primitive. |
| `metrics.py` | DeepEval wrappers (`task_completion`, `tool_correctness`) + `factuality_against_findings` for the newsroom quality gate. |
| `ab_test.py` | `run_ab(treatment, control, cases, score_fn)` returning `ABResult`. |

## How notebooks import it

The kit lives at the repo root (`shared/eval_kit/`). Each consuming
notebook adds one line to its setup cell:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parents[1] / "shared"))
from eval_kit.judge import LLMJudge
from eval_kit.metrics import task_completion, factuality_against_findings
from eval_kit.ab_test import run_ab
```

`Path.cwd().parents[1]` resolves the repo root from a `MM_module/labs/`
notebook. If a notebook lives elsewhere, adjust the `parents[N]` index.

## How it grows across modules

| Module | Lab | Uses |
|---|---|---|
| 01 | `qlora_finetuning.ipynb` | `LLMJudge` for Arabic civics rubric (first appearance). |
| 01 | `adaptation_decisions.ipynb` | `LLMJudge` as "second opinion" on student classifications. |
| 02b | `memory_pipeline.ipynb` | `LLMJudge` + `run_ab` for memory-on vs memory-off A/B. |
| 03 | `multi_agent_newsroom.ipynb` | `factuality_against_findings` inside the Analyst quality gate. |
| 03 | `observability_and_evaluation.ipynb` | `task_completion`, `tool_correctness`. |

## Environment

The judge model defaults to `openrouter/openai/gpt-4o-mini`. Override per
notebook with the `EVAL_JUDGE_MODEL` env var or by passing `model=` to
`LLMJudge` / `get_evaluator_model`.

## Why not the capstone's `project/src/evaluation/`?

That module is RAG-focused (`ContextualPrecisionMetric`, etc.) and depends
on `src.config.settings`. This kit is **agent-generic**, has no project
dependencies, and is sized to be read in one sitting. The two coexist.
