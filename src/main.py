import asyncio

import structlog
import typer

from src.agent.orchestration import OrchestratorAgent
from src.config import settings
from src.logger import configure_logging

configure_logging()
logger = structlog.get_logger()

app = typer.Typer(help="AI Research Agent CLI")


@app.command()
def research(
    query: str = typer.Argument(..., help="The research query to run."),
    model: str = typer.Option(None, help="LLM model to use (overrides settings)."),
    max_steps: int = typer.Option(settings.max_steps, help="Max ReAct steps."),
):
    """Run the AI research agent on a query."""
    # TODO:
    # 1. resolved_model = model or settings.model_name
    # 2. agent = OrchestratorAgent(model=resolved_model, max_steps=max_steps)
    # 3. result = asyncio.run(agent.run(query))
    # 4. print(result["answer"])
    print("Not implemented yet. Complete the TODO above.")


if __name__ == "__main__":
    app()
