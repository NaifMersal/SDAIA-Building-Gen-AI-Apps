"""
Lab 4 - Step 2: Semantic Tool Selector
======================================
Use embeddings to dynamically match user queries to the most relevant tools.
"""

import logging
import numpy as np
from litellm import embedding
from tools.registry import registry, Tool

logger = logging.getLogger(__name__)


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.
    
    Formula: similarity = (A · B) / (||A|| * ||B||)
    
    TODO: Implement this function.
    Hint: Use numpy for vector operations.
    
    Args:
        a: First vector (list of floats)
        b: Second vector (list of floats)
    
    Returns:
        float: Similarity score between 0.0 and 1.0
    """
    # --- YOUR CODE HERE ---
    pass
    # --- END YOUR CODE ---


def get_embedding_vector(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """
    Get embedding vector for a text string using LiteLLM.
    
    TODO: Implement this function.
    Hint: Use litellm.embedding() and extract the embedding from the response.
    
    Args:
        text: The text to embed
        model: The embedding model to use
    
    Returns:
        list[float]: The embedding vector
    """
    # --- YOUR CODE HERE ---
    pass
    # --- END YOUR CODE ---


class SemanticToolSelector:
    """
    Dynamically select tools based on semantic similarity
    between query and tool descriptions.
    """

    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        self.embedding_model = embedding_model
        self._tool_embeddings: dict[str, list[float]] = {}
        self._indexed = False

    def build_index(self):
        """
        Embed all registered tool descriptions.
        Call this once at startup (or when tools change).
        
        TODO: Implement this method.
        Steps:
        1. Get all tools from registry.get_all_tools()
        2. For each tool, create text: f"{tool.name}: {tool.description}"
        3. Batch all descriptions for a single embedding call (efficient)
        4. Store embeddings in self._tool_embeddings
        5. Set self._indexed = True
        """
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---

    def select_tools(self, query: str, top_k: int = 5) -> list[tuple[Tool, float]]:
        """
        Select the top-K most relevant tools for a query.

        TODO: Implement this method.
        Steps:
        1. Build index if not already indexed
        2. Embed the query using get_embedding_vector()
        3. For each tool, compute cosine similarity with query
        4. Sort by similarity (highest first)
        5. Return top K as list of (Tool, similarity_score) tuples

        Args:
            query: The user's query
            top_k: Number of tools to return

        Returns:
            List of (Tool, similarity_score) tuples, sorted by relevance.
        """
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---

    def get_tool_schemas(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Convenience method: get OpenAI-format schemas for the top-K tools.
        Ready to pass directly to litellm.completion(tools=...).

        TODO: Implement this method.
        Steps:
        1. Call select_tools() to get top tools
        2. Return list of tool.to_openai_schema() for each tool
        """
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---


if __name__ == "__main__":
    # Quick test
    from tools.registry import registry
    
    # Register some sample tools
    @registry.register("search", "Search for information on the web", "general")
    def search(query: str) -> str:
        return f"Results for: {query}"
    
    @registry.register("get_stock_price", "Get the current stock price", "financial")
    def get_stock_price(ticker: str) -> str:
        return f"Stock price for {ticker}: $100"
    
    selector = SemanticToolSelector()
    selector.build_index()
    
    tools = selector.select_tools("What is Apple's stock price?", top_k=2)
    for tool, score in tools:
        print(f"{tool.name}: {score:.4f}")
