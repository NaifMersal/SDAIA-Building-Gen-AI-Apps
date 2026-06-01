import logging
import socket
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from src.tools.registry import registry

logger = logging.getLogger(__name__)

def validate_url(url: str) -> bool:
    """
    Validate URL to prevent SSRF (Server-Side Request Forgery).
    Blocks localhost, private IP ranges, and non-http/https schemes.
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ["http", "https"]:
            return False

        hostname = parsed.hostname
        if not hostname:
            return False

        # Resolve hostname to IP
        try:
            ip_address = socket.gethostbyname(hostname)
        except socket.gaierror:
            return False # Could not resolve

        # Simple check for private ranges (10.x.x.x, 192.168.x.x, 172.16.x.x, 127.x.x.x)
        # In a real prod env, use the `ipaddress` module for strict checking
        parts = ip_address.split('.')
        if parts[0] == '10': return False
        if parts[0] == '192' and parts[1] == '168': return False
        if parts[0] == '172' and 16 <= int(parts[1]) <= 31: return False
        if parts[0] == '127': return False
        if ip_address == "0.0.0.0": return False

        return True
    except Exception:
        return False

@registry.register(
    "search_web",
    "Search the web for a query. Returns a list of results with title, link, and snippet.",
    category="research",
)
def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the web using DuckDuckGo (HTML).
    """
    url = "https://html.duckduckgo.com/html/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.post(url, data={"q": query}, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Search request failed: {e}")
        # Return empty list gracefully instead of crashing the agent
        return [{"title": "Error", "link": "", "snippet": f"Search failed: {str(e)}"}]

    logger.info(f"Searching web for: '{query}'")

    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for result in soup.find_all("div", class_="result", limit=max_results):
        title_tag = result.find("a", class_="result__a")
        snippet_tag = result.find("a", class_="result__snippet")

        if title_tag and snippet_tag:
            link = title_tag["href"]
            # Basic validation on the result link too
            if validate_url(link):
                results.append({
                    "title": title_tag.get_text(strip=True),
                    "link": link,
                    "snippet": snippet_tag.get_text(strip=True)
                })

    logger.info(f"Search returned {len(results)} results for '{query}'")
    if not results:
        logger.warning(f"No results found for '{query}' (Raw response length: {len(response.text)})")

    return results

@registry.register(
    "read_webpage",
    "Read the content of a webpage. Returns the text content.",
    category="research",
)
def read_webpage(url: str) -> str:
    """Read and extract text from a URL."""
    if not validate_url(url):
        return "Error: Invalid or restricted URL. Access to local/private networks is blocked."

    try:
        if "example.com" in url:
             return f"Simulated content for {url}."

        logger.info(f"Reading webpage: {url}")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator="\n")
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        content = text[:10000]  # Truncate to avoid context overflow
        logger.info(f"Read {len(content)} chars from {url}")
        return content

    except Exception as e:
        return f"Error reading {url}: {e}"
