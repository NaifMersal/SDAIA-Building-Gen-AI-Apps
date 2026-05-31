"""Thin DeepEval wrappers + agent-specific metrics.

Used by:
- Module 03 Lab 1 (observability & evaluation): task_completion, tool_correctness.
- Module 03 Lab 2 (newsroom): factuality_against_findings on writer drafts.
"""

from __future__ import annotations

import os
from typing import Optional

from deepeval.metrics import (
    BaseMetric,
    TaskCompletionMetric,
    ToolCorrectnessMetric,
)
from deepeval.models import LiteLLMModel
from deepeval.test_case import LLMTestCase

from eval_kit.judge import LLMJudge

DEFAULT_EVAL_MODEL = os.getenv("EVAL_JUDGE_MODEL", "openrouter/deepseek/deepseek-v4-flash:free")


def get_evaluator_model(model: Optional[str] = None) -> LiteLLMModel:
    return LiteLLMModel(model=model or DEFAULT_EVAL_MODEL, temperature=0)


def task_completion(
    threshold: float = 0.7, model: Optional[str] = None
) -> TaskCompletionMetric:
    return TaskCompletionMetric(threshold=threshold, model=get_evaluator_model(model))


def tool_correctness(threshold: float = 0.7) -> ToolCorrectnessMetric:
    return ToolCorrectnessMetric(threshold=threshold)


class FactualityAgainstFindings(BaseMetric):
    """Pass if every claim in the candidate is supported by the findings.

    Wraps `LLMJudge` so the same judge primitive students learn in Module 01
    flows through into DeepEval test runs. Reads `LLMTestCase.actual_output`
    as the candidate and `LLMTestCase.context` as the findings.
    """

    def __init__(self, threshold: float = 0.7, model: Optional[str] = None):
        self.threshold = threshold
        self.judge = LLMJudge(
            rubric=(
                "Does every factual claim in the candidate appear in the context "
                "findings? Score 1 only if all claims are grounded; otherwise 0."
            ),
            model=model,
            scale_max=1,
        )
        self.score: float = 0.0
        self.reason: str = ""
        self.success: bool = False

    def measure(self, test_case: LLMTestCase) -> float:
        findings = "\n".join(test_case.context or [])
        verdict = self.judge.score(test_case.actual_output, context=findings)
        self.score = float(verdict.score)
        self.reason = verdict.reasoning
        self.success = self.score >= self.threshold
        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> float:
        findings = "\n".join(test_case.context or [])
        verdict = await self.judge.ascore(test_case.actual_output, context=findings)
        self.score = float(verdict.score)
        self.reason = verdict.reasoning
        self.success = self.score >= self.threshold
        return self.score

    def is_successful(self) -> bool:
        return self.success

    @property
    def __name__(self) -> str:
        return "FactualityAgainstFindings"


def factuality_against_findings(
    threshold: float = 0.7, model: Optional[str] = None
) -> FactualityAgainstFindings:
    return FactualityAgainstFindings(threshold=threshold, model=model)
