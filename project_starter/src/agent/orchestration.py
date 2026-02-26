"""
Multi-agent orchestration layer.

Design and implement your own orchestration strategy here.
This file is entirely yours — there is no single correct answer.
"""

from src.agent.base import BaseAgent
from src.agent.prompts import (
    ANALYST_PROMPT,
    FACT_CHECKER_PROMPT,
    PLANNER_PROMPT,
    RESEARCHER_PROMPT,
    WRITER_PROMPT,
)
from src.config import settings


class OrchestratorAgent:
    """
    Your multi-agent orchestrator. Design your own pipeline.

    You have access to:
    - BaseAgent: a single ReAct agent you can instantiate with any system prompt
    - prompts.py: ready-made prompts (RESEARCHER_PROMPT, ANALYST_PROMPT,
      WRITER_PROMPT, FACT_CHECKER_PROMPT, PLANNER_PROMPT)
    - The tool registry: search_web and read_webpage are available once
      you've completed the tools/registry.py TODO.

    Ideas to get you started:
    - Chain researcher → analyst → writer in sequence
    - Run researcher and fact-checker in PARALLEL with asyncio.gather(),
      then synthesize their outputs
    - Build a retry loop: if confidence is low, re-run the researcher
    - Add a planner agent that breaks the query into sub-tasks first
    - Invent your own pattern!

    The only requirement: return {"answer": "...", "metadata": {...}}
    """

    def __init__(self, model: str = None, max_steps: int = 10):
        # TODO: Initialize the sub-agents you want to use.
        #
        # Example — a simple researcher:
        #
        #   resolved_model = model or settings.model_name
        #
        #   self.researcher = BaseAgent(
        #       model=resolved_model,
        #       max_steps=max_steps,
        #       agent_name="Researcher",
        #       system_prompt=RESEARCHER_PROMPT,
        #   )
        # You can add as many agents as you like.
        pass

    async def run(self, query: str) -> dict:
        # TODO: Implement your orchestration strategy.
        #
        # Example — sequential chain:
        #
        #   research_result = await self.researcher.run(query)
        #   research_output = research_result["answer"]
        #
        #   return {
        #       "answer": research_output["answer"],
        #       "metadata": {
        #           "researcher_trace": research_result["metadata"].get("trace_id"),
        #       },
        #   }
        #
        # Return {"answer": "...", "metadata": {...}} when done.
        pass
