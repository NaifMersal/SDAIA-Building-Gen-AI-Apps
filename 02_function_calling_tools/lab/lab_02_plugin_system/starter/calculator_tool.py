"""
CalculatorTool — Migrate the Calculator to the Plugin Pattern
=============================================================
Convert the calculator from Lab 1 into a BaseTool subclass,
making it compatible with the ToolRegistry.

Steps:
  1. Implement name, description, parameters properties
  2. Implement execute() with the arithmetic logic
"""

from typing import Dict, Any
from base import BaseTool


class CalculatorTool(BaseTool):
    """A calculator tool that performs basic arithmetic operations."""

    @property
    def name(self) -> str:
        # TODO: Return the tool name string "execute_calculation"
        pass

    @property
    def description(self) -> str:
        # TODO: Return a description for the LLM.
        # Make it specific: mention the operations, give a usage example.
        # E.g. "Executes basic arithmetic (add, subtract, multiply, divide, pow).
        #        Example: 15% of 200 → operation='multiply', operand_a=200, operand_b=0.15."
        pass

    @property
    def parameters(self) -> Dict[str, Any]:
        # TODO: Return the JSON Schema for the calculator inputs.
        # It must define three properties:
        #   - operation: string with enum ["add", "subtract", "multiply", "divide", "pow"]
        #   - operand_a: number
        #   - operand_b: number
        # All three are required.
        pass

    def execute(self, operation: str, operand_a: float, operand_b: float, **kwargs) -> Dict[str, Any]:
        """
        Perform the calculation.

        Returns:
            {"success": True/False, "result": <number or None>, "error": <str or None>}
        """
        # TODO: Implement the operation logic
        # - "add":      operand_a + operand_b
        # - "subtract": operand_a - operand_b
        # - "multiply": operand_a * operand_b
        # - "divide":   operand_a / operand_b (check for zero!)
        # - "pow":      operand_a ** operand_b
        # - else:       return error "Unsupported operation: {operation}"
        #
        # Wrap in try/except and always return structured dict
        pass


if __name__ == "__main__":
    calc = CalculatorTool()
    print(f"Name: {calc.name}")
    print(f"Schema: {calc.get_schema()}")
    print(f"Add:           {calc.execute(operation='add',      operand_a=10,  operand_b=5)}")
    print(f"Multiply:      {calc.execute(operation='multiply', operand_a=500, operand_b=0.15)}")
    print(f"Divide by zero:{calc.execute(operation='divide',   operand_a=10,  operand_b=0)}")
    print(f"Power:         {calc.execute(operation='pow',      operand_a=2,   operand_b=10)}")
