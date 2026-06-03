"""Shared utilities for Module 06 labs."""

_encoder = None


def get_encoder():
    """Return a cached SentenceTransformer instance (lazy-loaded on first call)."""
    global _encoder
    if _encoder is None:
        from sentence_transformers import SentenceTransformer
        print("Loading embedding model (one-time cost)...")
        _encoder = SentenceTransformer("all-MiniLM-L6-v2")
        print("Model loaded.")
    return _encoder


# Approximate pricing per 1M tokens (input + output combined).
# In production use litellm.completion_cost() for accurate per-call costs.
_PRICE_PER_1M = {
    "claude-haiku-4-5":    1.0 + 5.0,
    "claude-sonnet-4-6":   3.0 + 15.0,
    "claude-opus-4-7":    15.0 + 75.0,
}


def simulate_cost(tokens: int, model: str = "claude-sonnet-4-6") -> float:
    """Estimate cost in USD for `tokens` tokens on `model`.

    Uses a combined input+output rate as a rough simulation.
    Replace with litellm.completion_cost() for actual request costs.
    """
    rate = _PRICE_PER_1M.get(model, _PRICE_PER_1M["claude-sonnet-4-6"])
    return tokens * rate / 1_000_000
