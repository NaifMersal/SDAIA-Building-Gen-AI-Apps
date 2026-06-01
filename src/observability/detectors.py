import statistics
from dataclasses import dataclass
from datetime import date
from threading import Lock

from src.exceptions import TokenBudgetExceeded

@dataclass
class LoopDetectionResult:
    is_looping: bool
    strategy: str  # "exact", "fuzzy", "stagnation", "none"
    message: str
    confidence: float

class LoopDetector:
    """
    Detects agent loops using three strategies.
    """
    def __init__(
        self,
        exact_threshold: int = 2,
        fuzzy_threshold: float = 0.8,
        stagnation_window: int = 3,
    ):
        self.exact_threshold = exact_threshold
        self.fuzzy_threshold = fuzzy_threshold
        self.stagnation_window = stagnation_window
        self.tool_history: list[tuple[str, str]] = []  # (tool_name, args_str)
        self.output_history: list[str] = []

    def _jaccard_similarity(self, s1: str, s2: str) -> float:
        """
        Compute Jaccard similarity between two strings.
        Uses word-level tokens for meaningful comparison.
        """
        tokens1 = set(s1.lower().split())
        tokens2 = set(s2.lower().split())

        if not tokens1 and not tokens2:
            return 1.0
        if not tokens1 or not tokens2:
            return 0.0

        intersection = tokens1 & tokens2
        union = tokens1 | tokens2
        return len(intersection) / len(union)

    def check_tool_call(self, tool_name: str, tool_input: str) -> LoopDetectionResult:
        """
        Check if a tool call indicates a loop.
        Call this BEFORE executing the tool.
        """
        current = (tool_name, tool_input.strip())

        # Strategy 1: Exact Match
        exact_count = sum(
            1 for past_tool, past_input in self.tool_history
            if (past_tool, past_input.strip()) == current
        )

        if exact_count >= self.exact_threshold:
            self.tool_history.append(current)
            return LoopDetectionResult(
                is_looping=True,
                strategy="exact",
                message=(
                    f"Exact loop detected: '{tool_name}' called {exact_count + 1} "
                    f"times with identical arguments. Change your approach."
                ),
                confidence=1.0,
            )

        # Strategy 2: Fuzzy Match
        # Check against recent history for similar (but not identical) calls
        recent_history = self.tool_history[-5:]  # Last 5 calls
        fuzzy_matches = 0
        for past_tool, past_input in recent_history:
            if past_tool == tool_name:
                similarity = self._jaccard_similarity(tool_input, past_input)
                if similarity >= self.fuzzy_threshold:
                    fuzzy_matches += 1

        if fuzzy_matches >= self.exact_threshold:
            self.tool_history.append(current)
            return LoopDetectionResult(
                is_looping=True,
                strategy="fuzzy",
                message=(
                    f"Fuzzy loop detected: '{tool_name}' called with very similar "
                    f"arguments {fuzzy_matches + 1} times. The rephrasing isn't "
                    f"helping — try a completely different tool or approach."
                ),
                confidence=0.85,
            )

        self.tool_history.append(current)
        return LoopDetectionResult(
            is_looping=False,
            strategy="none",
            message="",
            confidence=0.0,
        )

    def check_output_stagnation(self, output: str) -> LoopDetectionResult:
        """
        Check if the agent's outputs are stagnating
        (producing very similar responses repeatedly).
        """
        self.output_history.append(output)

        if len(self.output_history) < self.stagnation_window:
            return LoopDetectionResult(
                is_looping=False, strategy="none",
                message="", confidence=0.0,
            )

        # Check similarity among the last N outputs
        recent = self.output_history[-self.stagnation_window:]
        similarities = []
        for i in range(len(recent)):
            for j in range(i + 1, len(recent)):
                sim = self._jaccard_similarity(recent[i], recent[j])
                similarities.append(sim)

        avg_similarity = sum(similarities) / len(similarities) if similarities else 0

        if avg_similarity >= self.fuzzy_threshold:
            return LoopDetectionResult(
                is_looping=True,
                strategy="stagnation",
                message=(
                    f"Output stagnation detected: last {self.stagnation_window} "
                    f"outputs are {avg_similarity:.0%} similar. The agent is "
                    f"not making progress. Try a different approach entirely."
                ),
                confidence=avg_similarity,
            )

        return LoopDetectionResult(
            is_looping=False, strategy="none",
            message="", confidence=0.0,
        )

    def reset(self):
        self.tool_history.clear()
        self.output_history.clear()


class CostAnomalyDetector:
    """
    Z-score anomaly detector for hourly LLM cost (slides section D).

    Accumulates a rolling window of hourly cost samples and flags when the
    current sample exceeds `z_threshold` standard deviations from the mean.
    """

    def __init__(self, window: int = 24, z_threshold: float = 2.5):
        self.history: list[float] = []
        self.window = window
        self.z_threshold = z_threshold

    def check(self, hourly_cost: float) -> bool:
        if len(self.history) < self.window:
            self.history.append(hourly_cost)
            return False

        mean = statistics.mean(self.history[-self.window:])
        stdev = statistics.stdev(self.history[-self.window:])
        z_score = (hourly_cost - mean) / (stdev or 1)

        self.history.append(hourly_cost)
        if abs(z_score) > self.z_threshold:
            print(f"Anomaly detected! Z-Score: {z_score:.2f}")
            return True
        return False


class BudgetGuard:
    """
    Enforce a daily API spend limit (slides section D).

    Thread-safe: uses a Lock so concurrent agent runs share the same counter.
    Raises TokenBudgetExceeded if a charge would push the daily total past
    `daily_limit_usd`. Budget resets at midnight (keyed by ISO date).
    """

    def __init__(self, daily_limit_usd: float, monthly_limit_usd: float):
        self.daily_limit = daily_limit_usd
        self.monthly_limit = monthly_limit_usd  # TODO: enforce monthly limit
        self._daily_spend: dict[str, float] = {}
        self._lock = Lock()

    def check_and_charge(self, cost_usd: float) -> bool:
        """Returns True if spend is allowed, raises TokenBudgetExceeded otherwise."""
        with self._lock:
            day_key = date.today().isoformat()
            day_spend = self._daily_spend.get(day_key, 0.0)

            if day_spend + cost_usd > self.daily_limit:
                raise TokenBudgetExceeded(
                    f"Daily budget ${self.daily_limit} reached"
                )

            self._daily_spend[day_key] = day_spend + cost_usd
            return True
