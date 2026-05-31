"""Shared evaluation kit used across Modules 01, 02b, and 03.

One growing artifact: introduced in Module 01 Lab 4 (LLM-judge for Arabic
civics), reused in Module 02b Lab 2 (memory A/B), culminated in Module 03's
quality gate and CI-gated tests. See README.md for the threading story.
"""

from eval_kit.judge import JudgeVerdict, LLMJudge
from eval_kit.metrics import (
    factuality_against_findings,
    get_evaluator_model,
    task_completion,
    tool_correctness,
)
from eval_kit.ab_test import ABResult, run_ab

__all__ = [
    "ABResult",
    "JudgeVerdict",
    "LLMJudge",
    "factuality_against_findings",
    "get_evaluator_model",
    "run_ab",
    "task_completion",
    "tool_correctness",
]
