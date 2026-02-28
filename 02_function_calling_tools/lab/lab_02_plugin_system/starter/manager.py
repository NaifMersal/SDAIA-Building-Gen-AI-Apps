"""
ToolRateLimiter — Token Bucket Rate Limiting
=============================================
Prevents abuse by limiting how often a tool can be called.
Uses a token bucket algorithm: tokens refill over time,
each call consumes one token.

Steps:
  1. Implement is_allowed()
"""

import time
from threading import Lock


class ToolRateLimiter:
    """
    A simple token-bucket style rate limiter.

    Attributes:
        calls_per_minute: Maximum calls allowed per minute
        allowance:        Current number of available tokens
        last_check:       Timestamp of the last check
    """

    def __init__(self, calls_per_minute: int = 30):
        self.calls_per_minute = calls_per_minute
        self.allowance = float(calls_per_minute)
        self.last_check = time.time()
        self.lock = Lock()

    def is_allowed(self) -> bool:
        """
        Returns True if the call is within the rate limit, False otherwise.

        Algorithm:
          1. Calculate time passed since last check
          2. Refill tokens: allowance += time_passed * (calls_per_minute / 60)
          3. Cap tokens at maximum (calls_per_minute)
          4. If allowance < 1 → deny (return False)
          5. Otherwise consume 1 token and allow (return True)
        """
        with self.lock:
            current = time.time()
            time_passed = current - self.last_check
            self.last_check = current

            # TODO: Refill tokens based on elapsed time
            # TODO: Cap at maximum
            # TODO: Check if we have a token to spend; consume and return True, else return False
            pass


if __name__ == "__main__":
    limiter = ToolRateLimiter(calls_per_minute=5)
    for i in range(8):
        allowed = limiter.is_allowed()
        print(f"Call {i+1}: {'Allowed' if allowed else 'BLOCKED'}")
