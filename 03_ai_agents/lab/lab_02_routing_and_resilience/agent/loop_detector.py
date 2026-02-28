"""
Lab 2 - Step 3: Advanced Loop Detector
========================================
"""

from dataclasses import dataclass

@dataclass
class LoopDetectionResult:
    is_looping: bool
    strategy: str   # "exact", "fuzzy", "stagnation", "none"
    message: str

class AdvancedLoopDetector:
    def __init__(self, exact_threshold: int = 2, fuzzy_threshold: float = 0.8, stagnation_window: int = 3):
        self.exact_threshold = exact_threshold
        self.fuzzy_threshold = fuzzy_threshold
        self.stagnation_window = stagnation_window
        self.tool_history: list[tuple[str, str]] = []
        self.output_history: list[str] = []

    def _jaccard_similarity(self, s1: str, s2: str) -> float:
        """TODO: Implement word-level Jaccard similarity (|intersection| / |union|)."""
        # --- YOUR CODE HERE ---
        return 0.0
        # --- END YOUR CODE ---

    def check_tool_call(self, tool_name: str, tool_input: str) -> LoopDetectionResult:
        """TODO: Check for exact and fuzzy loops."""
        # --- YOUR CODE HERE ---
        return LoopDetectionResult(False, "none", "")
        # --- END YOUR CODE ---

    def check_output_stagnation(self, output: str) -> LoopDetectionResult:
        """TODO: Check for repetitive reasoning outputs."""
        # --- YOUR CODE HERE ---
        return LoopDetectionResult(False, "none", "")
        # --- END YOUR CODE ---
