import logging

logger = logging.getLogger(__name__)

def search(query: str) -> str:
    """A search tool that returns errors for certain queries (simulates failure)."""
    mock_results = {
        "capital of france": "Paris is the capital of France.",
        "population of paris": "The population of Paris is approximately 2.1 million.",
        "python programming": "Python is a high-level programming language.",
    }
    query_lower = query.lower()
    for key, value in mock_results.items():
        if key in query_lower:
            return value

    # For unknown queries, returns an error that can trick an agent into looping
    return f"Error: No results found for '{query}'. Try searching with different keywords."


def calculate(expression: str) -> str:
    """Evaluate a math expression."""
    try:
        allowed = set('0123456789+-*/.(). ')
        if all(c in allowed for c in expression):
            return str(eval(expression))
        return "Error: Invalid expression"
    except Exception as e:
        return f"Error: {e}"

TOOLS_DICT = {"search": search, "calculate": calculate}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search for information. Returns text results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a math expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression"}
                },
                "required": ["expression"],
            },
        },
    },
]
