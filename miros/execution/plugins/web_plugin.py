"""Plugin handling web search and browser navigation intents."""

from __future__ import annotations

from miros.core.models import CommandResult, Intent, IntentCategory
from miros.execution.context import ExecutionContext
from miros.execution.plugins.base import CommandPlugin


class WebCommandPlugin(CommandPlugin):
    """Executes web commands."""

    name = "web"
    priority = 90

    def can_handle(self, intent: Intent) -> bool:
        return intent.category == IntentCategory.WEB

    def handle(self, intent: Intent, context: ExecutionContext) -> CommandResult:
        if intent.action == "web_search":
            result = context.web_executor.search(intent.entities["query"])
            return CommandResult(
                success=True,
                message=f"Searching the web for: {result['query']}",
                payload=result,
            )

        if intent.action == "open_url":
            result = context.web_executor.open_url(intent.entities["url"])
            return CommandResult(
                success=True,
                message=f"Opening {result['url']}",
                payload=result,
            )

        return CommandResult(
            success=False,
            message="Web command recognized but action is not implemented.",
            error=f"Unknown action: {intent.action}",
        )
