"""
Lab 1 - Steps 2 & 3: Plan-and-Execute Newsroom Agent
======================================================
Replace the rigid 4-phase pipeline with a dynamic planner that decides
WHICH steps to run and in WHAT order — no SharedWorkspace needed.
"""

import asyncio
import logging
from typing import List

from litellm import acompletion
from pydantic import BaseModel, Field

from config import MODEL_NAME
from specialists import call_specialist

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


# TODO: Write a planner prompt that instructs the LLM to decompose the query
#       into steps, each assigned to one of: "researcher", "analyst", "writer".
#       Include rules for when each specialist should be used and how to set depends_on.
PLANNER_PROMPT = """
# --- YOUR CODE HERE ---
# Hint: Explain the three specialists, their roles, and ask the LLM to produce
# a minimal ordered plan with step numbers and dependency lists.
# --- END YOUR CODE ---
"""


# ── Data models ───────────────────────────────────────────────────────────────
# These Pydantic models tell the LLM exactly what JSON shape to return.

class PlanStep(BaseModel):
    step: int = Field(..., description="Sequence number of the step.")
    task: str = Field(..., description="The specific, actionable task to perform.")
    specialist: str = Field(..., description="Specialist to use: 'researcher', 'analyst', or 'writer'.")
    depends_on: List[int] = Field(default_factory=list, description="Step numbers this step depends on.")


class Plan(BaseModel):
    steps: List[PlanStep] = Field(..., description="Ordered list of steps to achieve the goal.")


# ── Planner ───────────────────────────────────────────────────────────────────

class TaskPlanner:
    """Decomposes a newsroom query into ordered specialist sub-tasks."""

    async def create_plan(self, query: str) -> List[dict]:
        # TODO: Call acompletion with response_format=Plan and PLANNER_PROMPT.
        #       Parse the JSON response into a Plan object and return its steps as dicts.
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---


# ── Agent ─────────────────────────────────────────────────────────────────────

class NewsroomAgent:
    """
    A Plan-and-Execute newsroom agent.

    Phase 1 — Plan:    Decompose the query into specialist sub-tasks.
    Phase 2 — Execute: Run each sub-task with the right specialist,
                       passing dependency results as context.
    Phase 3 — Synthesize: Combine all step results into the final report.
    """

    def __init__(self):
        self.planner = TaskPlanner()

    def _get_context(self, step: dict, results: dict) -> str:
        """Build a context string from the results of dependency steps."""
        # TODO: Iterate over step["depends_on"], look up each dep in results,
        #       and join them into a formatted string.
        # --- YOUR CODE HERE ---
        return ""
        # --- END YOUR CODE ---

    async def run(self, query: str) -> dict:
        # Phase 1: Plan
        logger.info("Phase 1: Planning")
        plan = await self.planner.create_plan(query)

        for step in plan:
            logger.info(f"  Step {step['step']} [{step['specialist']}]: {step['task']}")

        # Phase 2: Execute
        logger.info("Phase 2: Executing")
        results = {}

        for step in plan:
            step_num = step["step"]
            specialist = step["specialist"]
            task = step["task"]

            # TODO: Get dependency context, build sub_task, call call_specialist,
            #       and store the result in results[step_num].
            # --- YOUR CODE HERE ---
            pass
            # --- END YOUR CODE ---

        # Phase 3: Synthesize
        logger.info("Phase 3: Synthesizing")
        final_answer = await self._synthesize(query, plan, results)

        return {
            "answer": final_answer,
            "metadata": {
                "plan": plan,
                "step_results": results,
            },
        }

    async def _synthesize(self, query: str, plan: list, results: dict) -> str:
        """Combine all step results into a final coherent answer."""
        # TODO: Format results_text as "Step N (task): answer" and call acompletion
        #       with a system prompt asking for a synthesized, cited final answer.
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---


async def main():
    agent = NewsroomAgent()
    result = await agent.run("Compare the environmental policies of the EU and US")
    print(f"\nFinal Report:\n{result['answer']}")


if __name__ == "__main__":
    asyncio.run(main())
