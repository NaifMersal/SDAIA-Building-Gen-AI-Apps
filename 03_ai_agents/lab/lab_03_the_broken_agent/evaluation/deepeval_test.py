"""
Lab 3 - Step 4: DeepEval Verification
======================================
Use DeepEval to verify the fixed agent works correctly.

Run with: pytest deepeval_test.py -v
Or use the CLI: python run_eval.py
"""

import os
import sys
from pathlib import Path

import pytest
from deepeval import evaluate
from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.metrics import TaskCompletionMetric, ToolCorrectnessMetric

sys.path.insert(0, str(Path(__file__).parent.parent / "solutions"))

from config import get_agent_metrics, DEFAULT_MODEL
from test_cases import load_test_cases, AgentTestCase
from runner import evaluate_agent, create_evaluation_report

from broken_agent import run_fixed_agent


class FixedAgentWrapper:
    """Wrapper to make the fixed agent compatible with evaluation infrastructure."""
    
    def __init__(self, model: str = None, max_steps: int = 10):
        self.model = model or DEFAULT_MODEL
        self.max_steps = max_steps
        self._last_result = None
    
    def run(self, query: str) -> str:
        result = run_fixed_agent(query, max_steps=self.max_steps)
        self._last_result = result
        return result.get("answer", "")
    
    def get_last_trace(self):
        if self._last_result:
            return type("Trace", (), {"total_steps": self._last_result.get("total_steps", 0)})()
        return None


@pytest.fixture
def agent():
    """Create a fixed agent instance for testing."""
    return FixedAgentWrapper(model="gpt-4o-mini", max_steps=10)


@pytest.fixture
def test_cases_json():
    """Path to the JSON test cases file."""
    return Path(__file__).parent / "test_cases.json"


class TestAgentFromJSON:
    """Tests loaded from JSON test cases file."""
    
    def test_factual_queries(self, agent, test_cases_json):
        """Agent should answer factual queries correctly."""
        cases = load_test_cases(str(test_cases_json))
        factual_cases = [c for c in cases if c.category == "factual"]
        
        for case in factual_cases:
            tc = case.to_llm_test_case()
            result = agent.run(case.input)
            tc.actual_output = result
            
            metric = TaskCompletionMetric(threshold=0.7)
            metric.measure(tc)
            
            assert metric.score >= 0.5, \
                f"Task completion failed for '{case.input}': score={metric.score}"
    
    def test_multi_step_queries(self, agent, test_cases_json):
        """Agent should handle multi-step reasoning."""
        cases = load_test_cases(str(test_cases_json))
        multi_step_cases = [c for c in cases if c.category == "multi_step"]
        
        for case in multi_step_cases:
            tc = case.to_llm_test_case()
            result = agent.run(case.input)
            tc.actual_output = result
            
            metrics = get_agent_metrics(threshold=0.6)
            task_metric, tool_metric, _ = metrics
            
            task_metric.measure(tc)
            assert task_metric.score >= 0.5, \
                f"Multi-step task failed for '{case.input}': score={task_metric.score}"


class TestLoopRecovery:
    """Tests for loop detection and recovery."""
    
    def test_respects_max_steps(self, agent):
        """Agent should not exceed max_steps even on difficult queries."""
        query = "Find extremely obscure information that might not exist anywhere"
        
        agent.run(query)
        
        trace = agent.get_last_trace()
        assert trace is not None
        assert trace.total_steps <= agent.max_steps, \
            f"Agent exceeded max_steps: {trace.total_steps} > {agent.max_steps}"


class TestToolCorrectness:
    """Tests for correct tool usage."""
    
    def test_uses_search_for_factual_queries(self, agent, test_cases_json):
        """Agent should use search tool for factual queries."""
        cases = load_test_cases(str(test_cases_json))
        factual_cases = [c for c in cases if c.category == "factual"]
        
        for case in factual_cases:
            tc = case.to_llm_test_case()
            result = agent.run(case.input)
            tc.actual_output = result
            
            metric = ToolCorrectnessMetric()
            metric.measure(tc)
            
            assert metric.score >= 0.3, \
                f"Tool correctness too low for '{case.input}': score={metric.score}"
    
    def test_uses_calculate_for_math(self, agent, test_cases_json):
        """Agent should use calculate tool for math operations."""
        cases = load_test_cases(str(test_cases_json))
        math_cases = [c for c in cases if c.category == "tool_correctness"]
        
        for case in math_cases:
            tc = case.to_llm_test_case()
            result = agent.run(case.input)
            tc.actual_output = result
            
            metric = ToolCorrectnessMetric()
            metric.measure(tc)
            
            assert metric.score >= 0.3, \
                f"Tool correctness too low for '{case.input}': score={metric.score}"


class TestEvaluationInfrastructure:
    """Tests for the evaluation infrastructure itself."""
    
    def test_load_test_cases(self, test_cases_json):
        """Test case loader should work correctly."""
        cases = load_test_cases(str(test_cases_json))
        assert len(cases) > 0, "No test cases loaded"
        
        for case in cases:
            assert case.input, "Test case missing input"
            assert case.expected_output, f"Test case '{case.input}' missing expected_output"
    
    def test_get_agent_metrics(self):
        """Metric factory should return valid metrics."""
        task, tool, answer = get_agent_metrics(threshold=0.7)
        
        assert task.threshold == 0.7
        assert tool.threshold == 0.7
        assert answer.threshold == 0.7
    
    def test_create_evaluation_report(self):
        """Report generator should work correctly."""
        results = {
            "num_test_cases": 2,
            "threshold": 0.7,
            "test_cases": [
                {"input": "Test 1", "actual_output": "Answer 1"},
                {"input": "Test 2", "actual_output": "Answer 2"},
            ]
        }
        
        report = create_evaluation_report(results)
        assert "# Agent Evaluation Report" in report
        assert "Test Cases**: 2" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
