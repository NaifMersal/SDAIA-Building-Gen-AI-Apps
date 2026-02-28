"""
BaseTool — Abstract Base Class for All Tools
==============================================
This file is COMPLETE. Read it carefully — it defines the contract
that every tool in the system must implement.

Every tool inherits from BaseTool and implements:
  - name:        unique identifier (e.g., 'execute_calculation')
  - description: LLM-facing explanation of when/how to use the tool
  - parameters:  JSON Schema for input arguments
  - permissions: list of required permissions (default: none)
  - execute():   the implementation logic
  - get_schema() is provided for you — no need to override it
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTool(ABC):
    """
    Abstract base class for all tools in the system.
    Enforces a standard structure for registration and execution.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The unique name of the tool (e.g., 'execute_calculation')."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """The explanation for the LLM on when/how to use this tool."""
        pass

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """The JSON Schema defining the tool's input arguments."""
        pass

    @property
    def permissions(self) -> list[str]:
        """
        List of permissions required to use this tool.
        Default is empty (no special permissions needed).

        Examples: ["filesystem:read"], ["database:query"], ["api:external"]
        """
        return []

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        The implementation logic.

        Must return a dict with keys: 'success', 'result', 'error'.
        Never raise an uncaught exception — always return structured errors.
        """
        pass

    def get_schema(self) -> Dict[str, Any]:
        """Returns the OpenAI-compatible tool schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
