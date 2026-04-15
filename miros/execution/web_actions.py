"""Web automation actions."""

from __future__ import annotations

import webbrowser
from typing import Any
from urllib.parse import quote_plus, urlparse


class WebActionExecutor:
    """Executes browser-oriented actions like opening URLs and searches."""

    def __init__(self, search_endpoint_template: str) -> None:
        self.search_endpoint_template = search_endpoint_template

    def open_url(self, url: str) -> dict[str, Any]:
        """Open a normalized URL in the default browser."""
        normalized = self._normalize_url(url)
        webbrowser.open(normalized)
        return {"url": normalized, "status": "opened"}

    def search(self, query: str) -> dict[str, Any]:
        """Search the web using configured search endpoint template."""
        encoded = quote_plus(query.strip())
        url = self.search_endpoint_template.format(query=encoded)
        webbrowser.open(url)
        return {"query": query, "search_url": url, "status": "opened"}

    @staticmethod
    def _normalize_url(url: str) -> str:
        cleaned = url.strip()
        parsed = urlparse(cleaned)
        if not parsed.scheme:
            return f"https://{cleaned}"
        return cleaned
