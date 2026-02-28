"""
Lab 2 - Step 1: Semantic Tool Selector
======================================
"""

import numpy as np
from litellm import embedding
from tools.registry import registry, Tool
from config import EMBEDDING_MODEL

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """TODO: Implement similarity = (A · B) / (||A|| * ||B||)"""
    # --- YOUR CODE HERE ---
    return 0.0
    # --- END YOUR CODE ---

def get_embedding_vector(text: str) -> list[float]:
    """Get embedding vector using LiteLLM."""
    response = embedding(model=EMBEDDING_MODEL, input=[text])
    return response.data[0]["embedding"]

class SemanticToolSelector:
    def __init__(self):
        self._tool_embeddings: dict[str, list[float]] = {}
        self._indexed = False

    def build_index(self):
        """TODO: Embed all registered tool descriptions."""
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---

    def select_tools(self, query: str, top_k: int = 5) -> list[tuple[Tool, float]]:
        """TODO: Select the top-K most relevant tools for a query."""
        # --- YOUR CODE HERE ---
        return []
        # --- END YOUR CODE ---

    def get_tool_schemas(self, query: str, top_k: int = 5) -> list[dict]:
        selected = self.select_tools(query, top_k)
        return [tool.to_openai_schema() for tool, _score in selected]
