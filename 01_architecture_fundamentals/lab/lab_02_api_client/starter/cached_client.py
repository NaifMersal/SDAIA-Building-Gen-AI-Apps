"""
Lab 2 — Step 5: Cached Client

Extends LiteLLMClient with local caching to minimize API calls.
Essential for development on free tier.

The cache directory setup and key generation are complete.
Complete the three TODOs in the query() method.
"""

import hashlib
import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from litellm_client import LiteLLMClient


class CachedLiteLLMClient(LiteLLMClient):
    """
    Extends LiteLLMClient with local caching to minimize API calls.
    """

    def __init__(self, cache_dir: str = ".cache/llm_responses"):
        super().__init__()
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_key(self, model_id: str, messages: list) -> str:
        """Generate a unique cache key from the request."""
        content = json.dumps({"model": model_id, "messages": messages}, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def query(self, model_id: str, messages: list, use_cache: bool = True, **kwargs) -> str:
        """Query with optional local caching."""
        cache_key = self._cache_key(model_id, messages)
        cache_file = self.cache_dir / f"{cache_key}.json"

        # =================================================================
        # TODO 1: Check cache — return cached response if available
        #
        # If use_cache is True AND cache_file.exists():
        #   - Print "[Cache HIT] Using cached response"
        #   - Read the file: cache_file.read_text(encoding="utf-8")
        #   - Parse JSON and return it: json.loads(...)["response"]
        # =================================================================

        # Your code here (cache check)

        # =================================================================
        # TODO 2: Make the API call (cache miss)
        #
        # - Print "[Cache MISS] Calling API..."
        # - Call the parent's query method: super().query(...)
        # - Store the result in a variable
        # =================================================================

        # Your code here (API call)
        result = None  # Replace with: super().query(model_id, messages, **kwargs)

        # =================================================================
        # TODO 3: Write result to cache
        #
        # - Convert result to JSON string: json.dumps({"response": result}, ensure_ascii=False)
        # - Write to cache_file: cache_file.write_text(..., encoding="utf-8")
        # =================================================================

        # Your code here (cache write)

        return result


# --- Main: demonstrate cache behavior ---
if __name__ == "__main__":
    client = CachedLiteLLMClient()

    model = "openrouter/meta-llama/llama-3-8b-instruct:free"
    messages = [{"role": "user", "content": "What is retrieval-augmented generation?"}]

    print("--- First call (should be Cache MISS) ---")
    result1 = client.query(model, messages)
    if result1:
        print(result1[:200])

    print("\n--- Second call (should be Cache HIT) ---")
    result2 = client.query(model, messages)
    if result2:
        print(result2[:200])
