from litellm import completion
from tools.registry import registry, Tool
from config import MODEL_NAME

ROUTER_SYSTEM_PROMPT = """You are a query router. Classify the user's query
into exactly one domain. Respond with ONLY the domain name, nothing else.

Available domains:
- "financial": Stock prices, currency conversion, crypto, market analysis
- "academic": Research papers, scientific definitions, citations, studies
- "general": Weather, web search, calculations, general knowledge

If unsure, respond with "general"."""

class ToolRouter:
    def __init__(self, router_model: str = "gpt-4o-mini"):
        self.router_model = router_model
        self.valid_domains = ["financial", "academic", "general"]

    def classify(self, query: str) -> str:
        response = completion(
            model=self.router_model,
            messages=[{"role": "system", "content": ROUTER_SYSTEM_PROMPT}, {"role": "user", "content": query}],
            max_tokens=20,
            temperature=0,
        )
        domain = response.choices[0].message.content.strip().lower().strip('"').strip("'")
        return domain if domain in self.valid_domains else "general"

    def route(self, query: str) -> tuple[str, list[Tool]]:
        domain = self.classify(query)
        return domain, registry.get_tools_by_category(domain)
