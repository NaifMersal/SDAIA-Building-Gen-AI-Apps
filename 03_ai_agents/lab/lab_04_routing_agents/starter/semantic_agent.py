"""
Lab 4 - Step 3: Semantic Agent
================================
An agent that dynamically retrieves the top-k most relevant tools
for every query using embeddings.
"""

import json
import logging
from litellm import completion
from routing.semantic_router import SemanticToolSelector

logger = logging.getLogger(__name__)

REACT_SYSTEM_PROMPT = """You are a research assistant agent. You solve tasks by
reasoning step-by-step and using tools when needed.

You have access to a set of tools.
ALWAYS use the provided tools to gather information or perform actions.
Never fabricate tool results.

When you have enough information to answer the user's question,
respond with your final answer."""


class SemanticAgent:
    """
    An agent that uses semantic routing to dynamically select tools
    for each query. This keeps the context window lean and improves
    tool selection accuracy.
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        embedding_model: str = "text-embedding-3-small",
        top_k: int = 5,
        max_steps: int = 10,
    ):
        """
        Initialize the SemanticAgent.
        
        TODO: Store parameters and create a SemanticToolSelector instance.
        """
        # --- YOUR CODE HERE ---
        pass
        # --- END YOUR CODE ---

    def run(self, user_query: str) -> dict:
        """
        Execute with semantic routing: embed query → select tools → run agent loop.
        
        TODO: Implement the full agent loop.
        Steps:
        1. Use self.selector.get_tool_schemas() to get relevant tools
        2. Log which tools were selected (for debugging)
        3. Run the standard agent loop with the filtered tools
        4. Return result dict with answer, selected_tools, and total_steps
        
        Returns:
            dict with keys: "answer", "selected_tools", "total_steps"
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
    
    agent = SemanticAgent(top_k=2)
    result = agent.run("What is Apple's stock price?")
    print(f"Answer: {result['answer']}")
    print(f"Tools used: {result.get('selected_tools', [])}")
