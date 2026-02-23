"""
Lab 2 — Steps 3 & 4: LiteLLMClient Class + Retry Logic

Step 3: Read the class structure — __init__ and helpers are complete.
Step 4: Complete the two TODOs inside the query() method.
"""

import os
import time
from dotenv import load_dotenv
from litellm import completion
from litellm.exceptions import RateLimitError, APIConnectionError, Timeout

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

class LiteLLMClient:
    """
    Production-ready client for the LiteLLM and OpenRouter APIs.
    Handles retries and rate limits.
    """

    def __init__(self, max_retries: int = 3, retry_delay: float = 5.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        # Ensure the key is loaded in environment for LiteLLM
        get_api_key()

    def query(self, model_id: str, messages: list, **kwargs) -> str:
        """
        Query a model with automatic retry logic.

        Handles:
        - RateLimitError: Rate limited — backs off exponentially
        - Network Errors: Timeout/Connection — retries with delay
        """
        for attempt in range(self.max_retries):
            try:
                response = completion(
                    model=model_id,
                    messages=messages,
                    timeout=120,
                    **kwargs
                )
                return response.choices[0].message.content

            except RateLimitError as e:
                # =============================================================
                # TODO 1: Handle RateLimitError
                #
                # When you've hit the rate limit.
                # - Calculate wait_time using exponential backoff:
                #   wait_time = self.retry_delay * (2 ** attempt)
                # - Print a message like: "Rate limited. Waiting Xs before retry..."
                # - Sleep for wait_time seconds
                # - Continue to the next attempt
                # =============================================================

                # Your code here (rate limit handling)
                pass

            except (APIConnectionError, Timeout) as e:
                # =============================================================
                # TODO 2: Handle network errors / timeout
                #
                # - Print: "Network error: {e}. Retrying (attempt N/max_retries)"
                # - If there are more attempts left, sleep for self.retry_delay
                #   and continue
                # - If this was the last attempt, raise the exception
                # =============================================================

                # Your code here (timeout handling)
                raise  # Remove this line once you implement the handler

            except Exception as e:
                # Other errors — raise immediately (e.g. AuthenticationError)
                raise RuntimeError(f"Unexpected error: {e}")

        raise RuntimeError(f"Failed after {self.max_retries} attempts.")

    # --- Helper methods (complete — no changes needed) ---

    def text_generation(
        self, prompt: str, model: str = "openrouter/meta-llama/llama-3-8b-instruct:free"
    ) -> str:
        """Generate text from a prompt."""
        return self.query(
            model_id=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )

    def summarization(
        self, text: str, model: str = "openrouter/mistralai/mistral-7b-instruct:free"
    ) -> str:
        """Summarize a long text into a shorter version."""
        prompt = f"Summarize this text concisely: {text}"
        return self.query(
            model_id=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=130,
            temperature=0.3
        )


# --- Main: test the methods ---
if __name__ == "__main__":
    client = LiteLLMClient()

    print("=== Text Generation ===")
    print(client.text_generation("List 3 benefits of using RAG in production systems:"))

    print("\n=== Summarization ===")
    long_text = (
        "Retrieval-Augmented Generation (RAG) is a technique that combines the power of "
        "large language models with external knowledge retrieval. Instead of relying solely "
        "on the model's training data, RAG systems first search a knowledge base for relevant "
        "documents, then use those documents as context for generating responses. This approach "
        "reduces hallucinations, keeps responses grounded in factual data, and allows the system "
        "to access information beyond the model's training cutoff date."
    )
    print(client.summarization(long_text))
