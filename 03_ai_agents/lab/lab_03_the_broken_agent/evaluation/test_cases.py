"""
Agent test case management for DeepEval evaluation.

Provides utilities for creating, loading, and managing test cases
for agent evaluation.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from deepeval.test_case import LLMTestCase, ToolCall
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentTestCase:
    """Structured test case for agent evaluation."""
    input: str
    expected_output: str
    expected_tools: List[str]
    category: str = "general"
    difficulty: str = "medium"

    def to_llm_test_case(self) -> LLMTestCase:
        """Convert to DeepEval LLMTestCase."""
        return LLMTestCase(
            input=self.input,
            expected_output=self.expected_output,
            tools_called=[
                ToolCall(name=tool, input_parameters={})
                for tool in self.expected_tools
            ]
        )


def load_test_cases(filepath: str) -> List[AgentTestCase]:
    """
    Load test cases from a JSON file.
    
    Expected format:
    [
        {
            "input": "What is the capital of France?",
            "expected_output": "Paris",
            "expected_tools": ["search"],
            "category": "factual",
            "difficulty": "easy"
        },
        ...
    ]
    
    Args:
        filepath: Path to JSON file with test cases
        
    Returns:
        List of AgentTestCase objects
    """
    path = Path(filepath)
    if not path.exists():
        logger.error(f"Test cases file not found: {filepath}")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    test_cases = [
        AgentTestCase(
            input=item['input'],
            expected_output=item.get('expected_output', ''),
            expected_tools=item.get('expected_tools', []),
            category=item.get('category', 'general'),
            difficulty=item.get('difficulty', 'medium'),
        )
        for item in data
    ]
    
    logger.info(f"Loaded {len(test_cases)} test cases from {filepath}")
    return test_cases


def save_test_cases(test_cases: List[dict], filepath: str) -> None:
    """
    Save test cases to a JSON file.
    
    Args:
        test_cases: List of test case dictionaries
        filepath: Path to save JSON file
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(test_cases)} test cases to {filepath}")


def create_sample_test_cases() -> List[dict]:
    """
    Create sample test cases for agent evaluation.
    
    Returns:
        List of sample test case dictionaries
    """
    return [
        {
            "input": "What is the capital of France?",
            "expected_output": "Paris",
            "expected_tools": ["search"],
            "category": "factual",
            "difficulty": "easy"
        },
        {
            "input": "What is the population of the capital of France?",
            "expected_output": "Paris has approximately 2.1 million people",
            "expected_tools": ["search", "search"],
            "category": "multi_step",
            "difficulty": "medium"
        },
        {
            "input": "What is the height of the Eiffel Tower?",
            "expected_output": "330 metres or 1083 feet",
            "expected_tools": ["search"],
            "category": "factual",
            "difficulty": "easy"
        },
        {
            "input": "What is 15 percent of 500?",
            "expected_output": "75",
            "expected_tools": ["calculate"],
            "category": "tool_correctness",
            "difficulty": "easy"
        },
        {
            "input": "Compare the population of Tokyo and Paris",
            "expected_output": "Tokyo has approximately 14 million people while Paris has 2.1 million",
            "expected_tools": ["search", "search"],
            "category": "multi_step",
            "difficulty": "medium"
        },
        {
            "input": "Search for python tutorial and summarize",
            "expected_output": "Information about Python tutorials",
            "expected_tools": ["search"],
            "category": "loop_recovery",
            "difficulty": "medium"
        }
    ]
