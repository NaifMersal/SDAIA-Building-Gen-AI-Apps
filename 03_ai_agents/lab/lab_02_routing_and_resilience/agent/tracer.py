"""
Lab 2 - Step 2: Agent Tracer
==============================
"""

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Optional

@dataclass
class ToolCallRecord:
    tool_name: str
    tool_input: dict
    tool_output: str
    duration_ms: float

@dataclass
class AgentStep:
    step_number: int
    reasoning: Optional[str]
    tool_calls: list[ToolCallRecord] = field(default_factory=list)
    duration_ms: float = 0.0
    timestamp: float = field(default_factory=time.time)

@dataclass
class Trace:
    trace_id: str
    agent_name: str
    input_query: str
    steps: list[AgentStep] = field(default_factory=list)
    status: str = "running"

class AgentTracer:
    def __init__(self, verbose: bool = True):
        self._traces: dict[str, Trace] = {}
        self.verbose = verbose

    def start_trace(self, agent_name: str, query: str) -> str:
        """TODO: Start a new trace."""
        # --- YOUR CODE HERE ---
        return ""
        # --- END YOUR CODE ---

    def log_step(self, trace_id: str, step: AgentStep):
        """TODO: Log a completed step."""
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---

    def end_trace(self, trace_id: str, status: str = "completed"):
        """TODO: Finalize the trace."""
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---

    def print_summary(self, trace_id: str):
        """TODO: Print a human-readable summary."""
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---
