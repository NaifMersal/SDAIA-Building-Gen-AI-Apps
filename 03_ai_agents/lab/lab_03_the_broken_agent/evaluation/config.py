"""
Agent evaluation configuration using DeepEval.

Provides LLM model configuration and metric factories for agent evaluation.
"""

import os
from typing import Optional

import litellm
from deepeval.metrics import (
    TaskCompletionMetric,
    ToolCorrectnessMetric,
    AnswerRelevancyMetric,
)
from deepeval.models import DeepEvalBaseLLM
import logging

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")


class LiteLLMModel(DeepEvalBaseLLM):
    """
    Wrapper for LiteLLM to work with DeepEval.
    
    DeepEval requires a specific interface for LLM evaluators.
    This wrapper enables using any LiteLLM-supported model.
    """

    def __init__(self, model: str = None) -> None:
        self.model = model or DEFAULT_MODEL

    def load_model(self) -> None:
        pass

    def generate(self, prompt: str) -> str:
        try:
            response = litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise

    async def a_generate(self, prompt: str) -> str:
        try:
            response = await litellm.acompletion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Async LLM generation failed: {e}")
            raise

    def get_model_name(self) -> str:
        return self.model


def get_evaluator_model(model: Optional[str] = None) -> LiteLLMModel:
    """Get the LLM model for evaluation."""
    model_name = model or DEFAULT_MODEL
    logger.info(f"Initializing evaluator model: {model_name}")
    return LiteLLMModel(model=model_name)


def get_agent_metrics(
    threshold: float = 0.7,
    model: Optional[str] = None
) -> tuple:
    """
    Get configured DeepEval metrics for agent evaluation.
    
    Args:
        threshold: Minimum score threshold for passing (0-1)
        model: LLM model to use for evaluation
        
    Returns:
        Tuple of (task_completion, tool_correctness, answer_relevancy)
    """
    evaluator = get_evaluator_model(model)
    
    task_completion = TaskCompletionMetric(
        threshold=threshold,
        model=evaluator,
        include_reason=True
    )
    
    tool_correctness = ToolCorrectnessMetric(
        threshold=threshold,
        model=evaluator,
        include_reason=True
    )
    
    answer_relevancy = AnswerRelevancyMetric(
        threshold=threshold,
        model=evaluator,
        include_reason=True
    )
    
    return task_completion, tool_correctness, answer_relevancy
