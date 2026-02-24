# Lab 3: The Broken Agent — Debugging Challenge

## Overview

You are given a **broken agent** that enters infinite loops and wastes tokens. Your job is to:

1. **Instrument** the agent with structured tracing
2. **Diagnose** the problem by reading trace logs
3. **Fix** the agent with a circuit breaker (loop detection)
4. **Verify** the fix works with DeepEval

## Learning Goals

1. Build an `AgentTracer` that captures every step of agent execution
2. Implement an `AdvancedLoopDetector` with exact, fuzzy, and stagnation detection
3. Integrate loop detection as a circuit breaker in the agent loop
4. Use DeepEval's `@observe` decorator for tracing and `TaskCompletionMetric` for evaluation

## Prerequisites

- `uv pip install -r requirements.txt`
- A valid API key in `.env` (e.g., `OPENAI_API_KEY=sk-...`)

## Files

```
starter/
  tracer.py           # TODO: Build the AgentTracer
  loop_detector.py    # TODO: Implement AdvancedLoopDetector
  broken_agent.py     # The broken agent (provided) + TODO: add circuit breaker

solutions/
  tracer.py           # Complete AgentTracer
  loop_detector.py    # Complete AdvancedLoopDetector
  broken_agent.py     # Fixed agent with circuit breaker

evaluation/
  deepeval_test.py    # DeepEval test cases for verification
```

## Steps

### Step 1: Build the Tracer (`starter/tracer.py`)

Implement the `AgentTracer` class with:
- `start_trace()` — begin a new trace
- `log_step()` — record a step with reasoning, tool calls, cost
- `end_trace()` — finalize with status
- `print_summary()` — human-readable output

### Step 2: Build the Loop Detector (`starter/loop_detector.py`)

Implement `AdvancedLoopDetector` with three strategies:
- **Exact Match** — same tool + same arguments repeated N times
- **Fuzzy Match** — Jaccard similarity on tool arguments (threshold: 0.8)
- **Output Stagnation** — agent outputs are too similar across steps

### Step 3: Fix the Broken Agent (`starter/broken_agent.py`)

The broken agent is provided — it loops on certain queries. Your job:
1. Inject the `AgentTracer` to see what's happening
2. Add the `AdvancedLoopDetector` as a circuit breaker
3. When a loop is detected, inject a warning message instead of executing the tool

### Step 4: Verify with DeepEval (`evaluation/deepeval_test.py`)

Run DeepEval to verify the fixed agent works correctly:

```bash
cd evaluation
pytest deepeval_test.py -v
```

This uses:
- `TaskCompletionMetric` — Did the agent accomplish the task?
- `ToolCorrectnessMetric` — Were the right tools called?

## Time

75 minutes

## Reference

Compare with the full project at:
`project/src/observability/tracer.py` and `project/src/observability/loop_detector.py`

## DeepEval Quick Reference

```python
from deepeval.tracing import observe
from deepeval import evaluate
from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.metrics import TaskCompletionMetric, ToolCorrectnessMetric

# Trace your agent
@observe(metrics=[TaskCompletionMetric(threshold=0.7)])
def run_agent(query: str) -> str:
    ...

# Evaluate with test cases
test_case = LLMTestCase(
    input="What is the population of Paris?",
    expected_output="approximately 2.1 million",
    tools_called=[ToolCall(name="search", args={"query": "population of Paris"})]
)
evaluate(test_cases=[test_case], metrics=[TaskCompletionMetric()])
```
