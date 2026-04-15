"""Routing utility to map intents to execution domains."""

from __future__ import annotations

from miros.core.models import Intent, IntentCategory


class IntentRouter:
    """Routes intents to plugin domains for observability and future policies."""

    def route(self, intent: Intent) -> str:
        """Resolve execution domain from intent category."""
        mapping = {
            IntentCategory.SYSTEM: "system",
            IntentCategory.WEB: "web",
            IntentCategory.API: "api",
            IntentCategory.CONVERSATION: "conversation",
            IntentCategory.UNKNOWN: "fallback",
        }
        return mapping.get(intent.category, "fallback")
