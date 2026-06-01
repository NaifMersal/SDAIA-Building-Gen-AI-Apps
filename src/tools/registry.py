import inspect
from typing import Any, Callable, Dict

from pydantic import BaseModel, create_model


class Tool:
    """A callable tool with schema."""

    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description
        self.model = self._create_pydantic_model(func)

    def _create_pydantic_model(self, func: Callable) -> type[BaseModel]:
        sig = inspect.signature(func)
        fields = {}
        for name, param in sig.parameters.items():
            if name == "self":
                continue
            annotation = param.annotation if param.annotation != inspect.Parameter.empty else str
            default = param.default
            fields[name] = (annotation, ...) if default == inspect.Parameter.empty else (annotation, default)
        return create_model(f"{self.name}Schema", **fields)

    def to_openai_schema(self) -> dict:
        schema = self.model.model_json_schema()
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": schema.get("properties", {}),
                    "required": schema.get("required", []),
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }

    def execute(self, **kwargs) -> Any:
        validated = self.model(**kwargs)
        return self.func(**validated.model_dump())


class ToolRegistry:
    """Registry for managing available tools."""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._categories: Dict[str, list[str]] = {}

    def register(self, name: str, description: str, category: str = "general"):
        """
        Decorator to register a function as a tool.

        Uses the Decorator Pattern to add registration to a function without
        modifying its implementation — the original function is returned unchanged
        so it can still be called directly.
        """
        def decorator(func: Callable):
            tool = Tool(name=name, func=func, description=description)
            self._tools[name] = tool
            self._categories.setdefault(category, []).append(name)
            return func

        return decorator

    def get_tool(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def get_all_tools(self) -> list[Tool]:
        return list(self._tools.values())

    def get_tools_by_category(self, category: str) -> list[Tool]:
        names = self._categories.get(category, [])
        return [self._tools[n] for n in names if n in self._tools]

    def execute_tool(self, name: str) -> Callable:
        tool = self.get_tool(name)
        return tool.execute if tool else None


# Global registry instance
registry = ToolRegistry()
