"""LLM-as-judge primitive.

Used by:
- Module 01 Lab 4 (QLoRA): grading Arabic civics outputs against the system
  prompt rubric (2 sentences, MSA, ends with the المصدر phrase).
- Module 01 Lab 3 (adaptation decisions): a 'second opinion' on student
  Prompt/RAG/Fine-tune classifications.
- Module 02b Lab 2 (memory pipeline): yes/no judge for the
  memory-on vs memory-off A/B.
- Module 03 Lab 2 (newsroom): factuality check of writer drafts against
  research findings (via `metrics.factuality_against_findings`).

The verdict shape (int score + reasoning) matches the slide vocabulary in
Module 03 Session 02 §F (LLM-as-judge with calibration).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Optional

import litellm


@dataclass
class JudgeVerdict:
    score: int
    reasoning: str

    @property
    def passed(self) -> bool:
        return self.score >= 1


DEFAULT_JUDGE_MODEL = os.getenv("EVAL_JUDGE_MODEL", "openrouter/deepseek/deepseek-v4-flash:free")


class LLMJudge:
    """Single-rubric LLM judge returning a structured verdict.

    Designed to be configured once and called many times against generations.
    Keep rubrics narrow — one yes/no question (or 0-1-2 rating) per judge.
    Stacking rubrics into one prompt degrades calibration; instantiate
    multiple LLMJudge objects instead.
    """

    def __init__(
        self,
        rubric: str,
        model: Optional[str] = None,
        scale_max: int = 1,
    ) -> None:
        self.rubric = rubric.strip()
        self.model = model or DEFAULT_JUDGE_MODEL
        self.scale_max = scale_max

    def _system_prompt(self) -> str:
        return (
            "You are a strict, deterministic evaluator. Return a JSON object "
            f'{{"score": <int 0..{self.scale_max}>, "reasoning": <str>}}. '
            "Score 0 means the criterion fails; the maximum score means it "
            "fully passes. Half-credit only if the rubric explicitly allows "
            "intermediate scores. Do not add any keys."
        )

    def _user_prompt(self, candidate: str, context: Optional[str]) -> str:
        parts = [f"# Rubric\n{self.rubric}"]
        if context:
            parts.append(f"# Context\n{context}")
        parts.append(f"# Candidate to evaluate\n{candidate}")
        return "\n\n".join(parts)

    def score(self, candidate: str, context: Optional[str] = None) -> JudgeVerdict:
        response = litellm.completion(
            model=self.model,
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": self._user_prompt(candidate, context)},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        return self._parse(raw)

    async def ascore(
        self, candidate: str, context: Optional[str] = None
    ) -> JudgeVerdict:
        response = await litellm.acompletion(
            model=self.model,
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": self._user_prompt(candidate, context)},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        return self._parse(raw)

    def _parse(self, raw: str) -> JudgeVerdict:
        try:
            data = json.loads(raw)
            score = int(data.get("score", 0))
            reasoning = str(data.get("reasoning", ""))
        except (json.JSONDecodeError, ValueError, TypeError):
            return JudgeVerdict(score=0, reasoning=f"unparseable judge output: {raw[:200]}")
        score = max(0, min(self.scale_max, score))
        return JudgeVerdict(score=score, reasoning=reasoning)
