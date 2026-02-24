"""
Evaluation runner for agent evaluation using DeepEval.

Provides utilities to run evaluations and generate reports.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from deepeval import evaluate
from deepeval.evaluate import DisplayConfig
from deepeval.test_case import LLMTestCase
import logging

from .config import get_agent_metrics
from .test_cases import AgentTestCase

logger = logging.getLogger(__name__)


def evaluate_agent(
    agent,
    test_cases: List[AgentTestCase],
    threshold: float = 0.7,
    model: Optional[str] = None
) -> dict:
    """
    Evaluate an agent using DeepEval metrics.
    
    Args:
        agent: The agent to evaluate (must have a run() method)
        test_cases: List of AgentTestCase objects
        threshold: Minimum passing score (0-1)
        model: LLM model for evaluation
        
    Returns:
        Dictionary with evaluation results
    """
    if not test_cases:
        logger.warning("No test cases provided for evaluation")
        return {"error": "No test cases provided"}
    
    logger.info(f"Starting agent evaluation with {len(test_cases)} test cases")
    
    metrics = get_agent_metrics(threshold, model)
    deepeval_cases: List[LLMTestCase] = []
    
    for i, case in enumerate(test_cases, 1):
        logger.info(f"Running test case {i}/{len(test_cases)}: {case.input[:50]}...")
        
        result = agent.run(case.input)
        
        tc = case.to_llm_test_case()
        tc.actual_output = result if isinstance(result, str) else result.get("answer", "")
        deepeval_cases.append(tc)
    
    results = evaluate(
        test_cases=deepeval_cases,
        metrics=list(metrics),
        display_config=DisplayConfig(print_results=True)
    )
    
    logger.info(f"Evaluation complete for {len(test_cases)} test cases")
    
    return {
        "num_test_cases": len(test_cases),
        "threshold": threshold,
        "results": results,
        "test_cases": [
            {"input": tc.input, "actual_output": tc.actual_output}
            for tc in deepeval_cases
        ]
    }


def run_evaluation_from_file(
    agent,
    test_cases_file: str,
    threshold: float = 0.7,
    model: Optional[str] = None
) -> dict:
    """
    Run evaluation using test cases from a file.
    
    Args:
        agent: The agent to evaluate
        test_cases_file: Path to JSON file with test cases
        threshold: Minimum passing score
        model: LLM model for evaluation
        
    Returns:
        Dictionary with evaluation results
    """
    from .test_cases import load_test_cases
    
    test_cases = load_test_cases(test_cases_file)
    
    if not test_cases:
        logger.error(f"No test cases loaded from {test_cases_file}")
        return {"error": f"No test cases loaded from {test_cases_file}"}
    
    return evaluate_agent(agent, test_cases, threshold, model)


def create_evaluation_report(results: dict, output_file: Optional[str] = None) -> str:
    """
    Create a human-readable evaluation report.
    
    Args:
        results: Evaluation results dictionary
        output_file: Optional file to save report
        
    Returns:
        Formatted report string
    """
    if "error" in results:
        return f"Evaluation Error: {results['error']}"
    
    lines = [
        "# Agent Evaluation Report",
        "",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Test Cases**: {results.get('num_test_cases', 0)}",
        f"**Threshold**: {results.get('threshold', 0.7)}",
        "",
        "## Results",
        "",
    ]
    
    eval_results = results.get("results")
    test_cases = results.get("test_cases", [])
    
    if eval_results and hasattr(eval_results, "test_results"):
        for i, (case, test_result) in enumerate(
            zip(test_cases, eval_results.test_results), 1
        ):
            lines.append(f"### Case {i}: {case.get('input', 'Unknown')[:60]}")
            lines.append(f"**Answer**: {case.get('actual_output', '')[:200]}")
            
            for metric_result in test_result.metrics_data:
                status = "PASS" if metric_result.success else "FAIL"
                lines.append(
                    f"- **{metric_result.name}**: {status} "
                    f"(score={metric_result.score:.3f}, threshold={metric_result.threshold})"
                )
                if metric_result.reason:
                    lines.append(f"  - Reason: {metric_result.reason}")
            lines.append("")
    else:
        lines.append("No detailed results available.")
    
    lines.extend([
        "",
        "## Recommendations",
        "- Review test cases with scores below threshold",
        "- Check tool correctness for failed cases",
        "- Consider adjusting agent prompts for edge cases",
    ])
    
    report = "\n".join(lines)
    
    if output_file:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"Evaluation report saved to {output_file}")
    
    return report
