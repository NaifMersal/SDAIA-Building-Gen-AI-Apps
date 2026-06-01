"""
BaseAgent: a ReAct agent with decorator-based observability.

Observability uses the same @observe / propagate_attributes API as production Langfuse.
Swapping to real Langfuse requires only changing the import:
    from langfuse import observe, propagate_attributes
"""

import asyncio
import json

import structlog
from litellm import acompletion, completion_cost
from pydantic import ValidationError

from src.agent.prompts import DEFAULT_SYSTEM_PROMPT
from src.config import settings
from src.observability.detectors import LoopDetector
from src.observability.observe import observe, propagate_attributes

logger = structlog.get_logger()


class BaseAgent:
    """
    A ReAct agent with full observability:
    - Decorator-based tracing of every call (@observe)
    - Loop detection (exact, fuzzy, stagnation)
    - Per-run cost tracking
    - Async execution
    """

    def __init__(
        self,
        model: str | None = None,
        max_steps: int = 10,
        agent_name: str = "BaseAgent",
        verbose: bool = True,
        system_prompt: str | None = None,
        tools: list | None = None,
    ):
        self.model = model or settings.model_name
        self.max_steps = max_steps
        self.agent_name = agent_name
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.verbose = verbose


        self.tools = tools or []
        self.tools_schema = [tool.to_openai_schema() for tool in self.tools]
        self.loop_detector = LoopDetector()


    @observe(name="agent_run", as_type="agent")
    async def run(self, user_query: str) -> dict:
        with propagate_attributes(metadata={"user_query": user_query}):
            """
            Execute the ReAct (Reasoning + Acting) loop to answer a user query.

            TODO: Implement the ReAct loop logic here.
            1. Initialize message history with the system prompt and user query.
            2. Use `propagate_attributes` to record the model name and any metadata.
            3. Loop up to self.max_steps:
                a. Call the LLM (acompletion) with tools and current messages.
                b. Track cost/usage from the response.
                c. If the LLM returns a final answer (no tool calls), return it.
                d. If there are tool calls:
                   - Append the assistant message to history.
                   - Execute the tools using self._execute_tool.
                   - Append tool results to history.
            4. Return the final answer and metadata.
            """
            # Start your implementation here...
            raise NotImplementedError("ReAct loop not implemented yet.")

    @observe(name="tool_call", as_type="tool")
    async def _execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Registry lookup + loop detection + asyncio.to_thread + error handling."""
        # NOTE: @observe automatically captures tool_name and arguments as 'input'
        # and the return value as 'output'. We only use propagate_attributes here 
        # if we need to pass session_id, user_id, or other context to child spans.

        loop_check = self.loop_detector.check_tool_call(tool_name, json.dumps(arguments))
        if loop_check.is_looping:
            logger.warning(
                "loop_detected",
                tool=tool_name,
                strategy=loop_check.strategy,
                message=loop_check.message,
            )
            result = f"SYSTEM: {loop_check.message} (Detection: {loop_check.strategy})"
            return result

        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            logger.error("tool_not_found", tool=tool_name)
            result = f"Error: Tool '{tool_name}' not found on this agent."
            return result

        try:
            result = str(await asyncio.to_thread(tool.execute, **arguments))
        except ValidationError as e:
            logger.warning("tool_validation_failed", tool=tool_name, error=str(e))
            result = f"Error: Tool arguments validation failed. {e}"
        except Exception as e:
            logger.error("tool_execution_failed", tool=tool_name, error=str(e))
            result = f"Error: {type(e).__name__}: {e}"

        return result
