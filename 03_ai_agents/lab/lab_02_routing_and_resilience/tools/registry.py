from typing import Callable, Any, Dict
from pydantic import BaseModel, create_model
import inspect

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
            if name == "self": continue
            annotation = param.annotation if param.annotation != inspect.Parameter.empty else str
            fields[name] = (annotation, ... if param.default == inspect.Parameter.empty else param.default)
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
                "strict": True
            },
        }

    def execute(self, **kwargs) -> Any:
        validated_args = self.model(**kwargs)
        return self.func(**validated_args.model_dump())

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._categories: Dict[str, list[str]] = {}

    def register(self, name: str, description: str, category: str = "general"):
        def decorator(func: Callable):
            tool = Tool(name, func, description)
            self._tools[name] = tool
            if category not in self._categories: self._categories[category] = []
            self._categories[category].append(name)
            return func
        return decorator

    def get_tool(self, name: str) -> Tool | None: return self._tools.get(name)
    def get_all_tools(self) -> list[Tool]: return list(self._tools.values())
    def get_tools_by_category(self, category: str) -> list[Tool]:
        return [self._tools[name] for name in self._categories.get(category, [])]

registry = ToolRegistry()
