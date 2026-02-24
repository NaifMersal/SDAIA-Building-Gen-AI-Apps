#!/usr/bin/env python
"""
Agent evaluation CLI script using DeepEval metrics.

Runs evaluation on a fixed agent using test cases from a JSON file.

Usage:
    python run_eval.py
    python run_eval.py --test-cases test_cases.json --model gpt-4o-mini
    python run_eval.py --output report.md
"""

import os
import sys
from pathlib import Path

import typer
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent / "solutions"))

from config import DEFAULT_MODEL
from runner import run_evaluation_from_file, create_evaluation_report
from test_cases import save_test_cases, create_sample_test_cases

app = typer.Typer(help="Evaluate the fixed agent with DeepEval metrics.")


@app.command()
def main(
    test_cases: Path = typer.Option(
        Path(__file__).parent / "test_cases.json",
        "--test-cases",
        help="Path to JSON test cases file.",
    ),
    model: str = typer.Option(
        None,
        "--model",
        help=f"Agent model (defaults to MODEL_NAME env var or {DEFAULT_MODEL}).",
    ),
    eval_model: str = typer.Option(
        None,
        "--eval-model",
        help="Model used for DeepEval metric evaluation.",
    ),
    output: Path = typer.Option(
        Path(__file__).parent / "evaluation_report.md",
        "--output",
        help="Output path for the evaluation report.",
    ),
    threshold: float = typer.Option(
        0.7,
        "--threshold",
        help="Minimum score threshold for passing.",
    ),
    create_samples: bool = typer.Option(
        False,
        "--create-samples",
        help="Create sample test cases file if it doesn't exist.",
    ),
) -> None:
    """Run DeepEval evaluation on the fixed agent."""
    typer.echo("=" * 60)
    typer.echo("Agent Evaluation with DeepEval")
    typer.echo("=" * 60)
    
    if not test_cases.exists():
        if create_samples:
            typer.echo(f"Creating sample test cases at {test_cases}")
            samples = create_sample_test_cases()
            save_test_cases(samples, str(test_cases))
        else:
            typer.echo(f"[ERROR] Test cases file not found: {test_cases}", err=True)
            typer.echo("Use --create-samples to generate sample test cases.")
            raise typer.Exit(code=1)
    
    typer.echo(f"Test cases: {test_cases}")
    typer.echo(f"Evaluation model: {eval_model or DEFAULT_MODEL}")
    typer.echo(f"Threshold: {threshold}")
    typer.echo("")
    
    typer.echo("Importing fixed agent...")
    try:
        from broken_agent import run_fixed_agent
        
        class AgentWrapper:
            def __init__(self):
                self.max_steps = 10
            
            def run(self, query: str) -> str:
                result = run_fixed_agent(query, max_steps=self.max_steps)
                return result.get("answer", "")
            
            def get_last_trace(self):
                return None
        
        agent = AgentWrapper()
    except ImportError as e:
        typer.echo(f"[ERROR] Could not import agent: {e}", err=True)
        raise typer.Exit(code=1)
    
    typer.echo("Running evaluation...")
    typer.echo("")
    
    results = run_evaluation_from_file(
        agent=agent,
        test_cases_file=str(test_cases),
        threshold=threshold,
        model=eval_model,
    )
    
    typer.echo("")
    typer.echo("Generating report...")
    report = create_evaluation_report(results, output_file=str(output))
    
    typer.echo("")
    typer.echo("=" * 60)
    typer.echo("Evaluation Complete")
    typer.echo("=" * 60)
    typer.echo(report)
    typer.echo(f"\nReport saved to: {output}")


if __name__ == "__main__":
    app()
