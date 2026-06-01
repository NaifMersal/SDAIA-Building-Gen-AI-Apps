"""
Prometheus metrics stub for the research agent.

If `prometheus_client` is not installed, all metric calls become silent no-ops.
Install the package to get real metrics:
    pip install -e '.[observability]'

FastAPI /metrics mount (from slides):
    from prometheus_client import make_asgi_app
    from fastapi import FastAPI

    app = FastAPI()
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
    # Prometheus scrapes: GET http://api:8000/metrics
    # → agent_requests_total{model="gpt-4o",cache_hit="false"} 1423
"""

try:
    from prometheus_client import Counter, Histogram
    _PROMETHEUS_AVAILABLE = True
except ImportError:
    _PROMETHEUS_AVAILABLE = False

    class _NoOpMetric:
        def __init__(self, *args, **kwargs):
            pass

        def labels(self, *args, **kwargs):
            return self

        def inc(self, amount=1):
            pass

        def observe(self, amount):
            pass

    Counter = _NoOpMetric      # type: ignore[misc,assignment]
    Histogram = _NoOpMetric    # type: ignore[misc,assignment]


class PrometheusMetrics:
    """
    Central registry of the four agent-level Prometheus metrics from the slides.

    Metrics
    -------
    agent_requests_total       Counter   labels: model, cache_hit, status
    agent_request_latency_ms   Histogram labels: (none)
    agent_tokens_total         Counter   labels: model, token_type
    agent_cost_usd_total       Counter   labels: model
    """

    def __init__(self):
        self.agent_requests_total = Counter(
            "agent_requests_total",
            "Total number of agent requests completed",
            ["model", "cache_hit", "status"],
        )
        self.agent_request_latency_ms = Histogram(
            "agent_request_latency_ms",
            "End-to-end request latency in milliseconds",
        )
        self.agent_tokens_total = Counter(
            "agent_tokens_total",
            "Cumulative token usage by type",
            ["model", "token_type"],
        )
        self.agent_cost_usd_total = Counter(
            "agent_cost_usd_total",
            "Cumulative API spend in USD",
            ["model"],
        )

    def record_request(
        self,
        model: str,
        status: str,
        latency_ms: float,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float,
        cache_hit: bool = False,
    ) -> None:
        """Convenience method — call once per completed LLM request."""
        cache_hit_str = str(cache_hit).lower()

        self.agent_requests_total.labels(
            model=model, cache_hit=cache_hit_str, status=status
        ).inc()

        self.agent_request_latency_ms.observe(latency_ms)

        self.agent_tokens_total.labels(model=model, token_type="input").inc(input_tokens)
        self.agent_tokens_total.labels(model=model, token_type="output").inc(output_tokens)

        self.agent_cost_usd_total.labels(model=model).inc(cost_usd)


# Module-level singleton — import this rather than constructing your own.
metrics = PrometheusMetrics()
