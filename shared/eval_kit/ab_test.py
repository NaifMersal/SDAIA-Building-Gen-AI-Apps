"""Minimal A/B helper for paired treatment vs control comparisons.

Used by Module 02b Lab 2 to run the memory-on vs memory-off A/B test
that Slide §G points students at.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean, pstdev
from typing import Any, Callable, Iterable, List


@dataclass
class ABResult:
    treatment_scores: List[float] = field(default_factory=list)
    control_scores: List[float] = field(default_factory=list)
    deltas: List[float] = field(default_factory=list)

    @property
    def mean_delta(self) -> float:
        return mean(self.deltas) if self.deltas else 0.0

    @property
    def treatment_mean(self) -> float:
        return mean(self.treatment_scores) if self.treatment_scores else 0.0

    @property
    def control_mean(self) -> float:
        return mean(self.control_scores) if self.control_scores else 0.0

    @property
    def wins(self) -> int:
        return sum(1 for d in self.deltas if d > 0)

    @property
    def losses(self) -> int:
        return sum(1 for d in self.deltas if d < 0)

    @property
    def ties(self) -> int:
        return sum(1 for d in self.deltas if d == 0)

    def summary(self) -> str:
        n = len(self.deltas)
        if n == 0:
            return "ABResult: no cases run."
        stdev = pstdev(self.deltas) if n > 1 else 0.0
        return (
            f"ABResult over {n} cases | "
            f"treatment={self.treatment_mean:.3f}  control={self.control_mean:.3f}  "
            f"delta={self.mean_delta:+.3f} (stdev={stdev:.3f}) | "
            f"wins={self.wins} losses={self.losses} ties={self.ties}"
        )


def run_ab(
    treatment_fn: Callable[[Any], Any],
    control_fn: Callable[[Any], Any],
    cases: Iterable[Any],
    score_fn: Callable[[Any, Any], float],
) -> ABResult:
    """Run a paired A/B test.

    For each case, runs both `treatment_fn(case)` and `control_fn(case)`,
    scores each output with `score_fn(case, output)`, and records the delta.

    `score_fn` typically wraps an `LLMJudge.score(...).score` call so the
    judge stays the single source of truth across modules.
    """
    result = ABResult()
    for case in cases:
        t_out = treatment_fn(case)
        c_out = control_fn(case)
        t_score = float(score_fn(case, t_out))
        c_score = float(score_fn(case, c_out))
        result.treatment_scores.append(t_score)
        result.control_scores.append(c_score)
        result.deltas.append(t_score - c_score)
    return result
