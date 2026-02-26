"""
BaseAgent: a ReAct agent with built-in observability.

Complete sections are marked COMPLETE.
The core run() method is marked TODO — that is your main implementation challenge.
"""

import asyncio
import json
import time
from typing import Optional

import structlog
from litellm import acompletion, completion_cost
from pydantic import ValidationError

from src.agent.prompts import DEFAULT_SYSTEM_PROMPT
from src.config import settings
from src.observability.loop_detector import AdvancedLoopDetector
from src.observability.tracer import AgentStep, AgentTracer, ToolCallRecord
from src.tools.registry import registry

logger = structlog.get_logger()


class BaseAgent:
    """
    A ReAct agent with full observability:
    - Structured tracing of every step
    - Loop detection (exact, fuzzy, stagnation)
    - Per-step cost tracking
    - Async execution with parallel tool calling
    """

    # ── COMPLETE: __init__ ────────────────────────────────────────────────

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

        if tools is None:
            self.tools = registry.get_all_tools()
        else:
            self.tools = tools

        self.tools_schema = [tool.to_openai_schema() for tool in self.tools]

        # Observability stack
        self.tracer = AgentTracer(verbose=verbose)
        self.loop_detector = AdvancedLoopDetector()

        # Shared state across hooks within a single run()
        self._current_trace_id: Optional[str] = None

    # ── COMPLETE: Tool execution ───────────────────────────────────────────

    async def _execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Registry lookup + loop detection + asyncio.to_thread + error handling."""
        # Check for loops BEFORE executing
        loop_check = self.loop_detector.check_tool_call(
            tool_name, json.dumps(arguments)
        )
        if loop_check.is_looping:
            logger.warning(
                "loop_detected",
                tool=tool_name,
                strategy=loop_check.strategy,
                message=loop_check.message,
            )
            return (
                f"SYSTEM: {loop_check.message} "
                f"(Detection: {loop_check.strategy})"
            )

        tool = registry.get_tool(tool_name)
        if not tool:
            logger.error("tool_not_found", tool=tool_name)
            return f"Error: Tool '{tool_name}' not found."
        try:
            result = await asyncio.to_thread(tool.execute, **arguments)
            return str(result)
        except ValidationError as e:
            logger.warning("tool_validation_failed", tool=tool_name, error=str(e))
            return f"Error: Tool arguments validation failed. {e}"
        except Exception as e:
            logger.error("tool_execution_failed", tool=tool_name, error=str(e))
            return f"Error: {type(e).__name__}: {e}"

    # ── COMPLETE: Hooks ────────────────────────────────────────────────────

    def _on_step_start(self, step: int, messages: list) -> None:
        """Called at the start of each ReAct step. Override to add custom behaviour."""
        pass

    def _on_tool_result(
        self, step: int, name: str, args: dict, result: str, duration_ms: float
    ) -> None:
        """Called after each tool result is received. Override to add custom behaviour."""
        pass

    def _on_step_end(
        self, step: int, response, tool_calls: list, step_duration_ms: float
    ) -> None:
        """
        Log a completed step to the tracer and record per-step cost.

        tool_calls is a list of (name, args, result, duration_ms) tuples
        accumulated during this step.
        """
        message = response.choices[0].message

        usage = response.usage
        input_tokens = usage.prompt_tokens if usage else 0
        output_tokens = usage.completion_tokens if usage else 0

        try:
            step_cost = completion_cost(completion_response=response)
        except Exception:
            step_cost = 0.0

        tool_records = [
            ToolCallRecord(
                tool_name=name,
                tool_input=args,
                tool_output=result,
                duration_ms=dur_ms,
            )
            for name, args, result, dur_ms in tool_calls
        ]

        agent_step = AgentStep(
            step_number=step,
            reasoning=message.content,
            tool_calls=tool_records,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=step_cost,
            duration_ms=step_duration_ms,
        )
        self.tracer.log_step(self._current_trace_id, agent_step)

    def _on_loop_end(
        self,
        answer: str,
        total_steps: int,
        status: str = "success",
        error: Optional[str] = None,
    ) -> None:
        """Finalise the trace when the ReAct loop exits (normally or on error)."""
        end_kwargs = {}
        if status != "success":
            end_kwargs["status"] = status
        if error:
            end_kwargs["error"] = error
        self.tracer.end_trace(self._current_trace_id, answer, **end_kwargs)

    # ── TODO: run() ───────────────────────────────────────────────────────

    async def run(self, user_query: str) -> dict:
        """
        Execute the ReAct (Reasoning + Acting) loop to answer a user query.

        The agent iteratively:
        1. Reasons about the current state/query.
        2. Decides to call tools or provide a final answer.
        3. Observes tool outputs and repeats until a solution is found or max steps are reached.

        Returns:
            dict: {
                "answer": str,
                "metadata": {
                    "trace_id": str,
                    "total_steps": int
                }
            }
        """
        # TODO: Remove this line and implement the steps above.
        raise NotImplementedError(
            "Implement the ReAct loop in BaseAgent.run(). "
            "Follow the step-by-step docstring above."
        )
