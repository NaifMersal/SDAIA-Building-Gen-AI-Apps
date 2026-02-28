"""
Lab 1 - Step 1: Specialist Agents for the Newsroom
====================================================
Define focused system prompts and a single dispatch function.
Each specialist should REFUSE to do work outside its niche.
"""

from litellm import completion
from config import MODEL_NAME


# TODO: Fill in each specialist's system prompt.
# Constraints are key — a good specialist should refuse work outside its role.
SPECIALIST_PROMPTS = {
    "researcher": """
    # --- YOUR CODE HERE ---
    # Write a system prompt for the Researcher specialist.
    # Hint: Tell it to ONLY research, cite sources, and return raw findings.
    # --- END YOUR CODE ---
    """,

    "analyst": """
    # --- YOUR CODE HERE ---
    # Write a system prompt for the Analyst specialist.
    # Hint: Tell it to evaluate info, flag contradictions, rate confidence.
    # --- END YOUR CODE ---
    """,

    "writer": """
    # --- YOUR CODE HERE ---
    # Write a system prompt for the Writer specialist.
    # Hint: Tell it to write clearly, preserve citations, be concise.
    # --- END YOUR CODE ---
    """,
}


def call_specialist(specialist: str, task: str) -> str:
    """Invoke a named specialist with a task and return its response."""
    # TODO: Look up the system prompt for `specialist` from SPECIALIST_PROMPTS,
    #       call the LLM, and return the response content.
    # --- YOUR CODE HERE ---
    pass
    # --- END YOUR CODE ---
