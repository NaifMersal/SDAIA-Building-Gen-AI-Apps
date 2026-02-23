"""
Lab 2 — Steps 1 & 2: Environment Setup + First API Call

Step 1: Read through the get_api_key() function — understand why we
        never hardcode tokens.
Step 2: Complete the TODO at the bottom to make your first API call.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_api_key():
    """Retrieve API token with validation."""
    token = os.getenv("OPENROUTER_API_KEY")
    if not token:
        raise EnvironmentError(
            "OPENROUTER_API_KEY not found. "
            "Create a .env file with your token or set the environment variable."
        )
    return token


# --- Configuration ---
TOKEN = get_api_key()
# We prefix the model with 'openrouter/' so LiteLLM knows where to route the request
MODEL_ID = "openrouter/meta-llama/llama-3-8b-instruct:free"

# =====================================================================
# TODO (Step 2): Make your first API call
#
# Import litellm's completion function and use it to send a request to OpenRouter.
#
# Hints:
#   - from litellm import completion
#   - Call completion()
#   - Pass `model=MODEL_ID`
#   - Pass `messages=[{"role": "user", "content": prompt}]`
#   - Key parameters: max_tokens=150, temperature=0.7
#   - The generated text is at response.choices[0].message.content
# =====================================================================

prompt = "Explain what a vector database is in one paragraph:"

# Your code here:
# try:
#     response = completion(...)
#     result_text = response.choices[0].message.content
#     print("Generated Text:")
#     print(result_text)
# except Exception as err:
#     print(f"An error occurred: {err}")
