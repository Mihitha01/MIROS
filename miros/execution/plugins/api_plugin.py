"""Plugin handling external API-like requests."""

from __future__ import annotations

from miros.core.models import CommandResult, Intent, IntentCategory
from miros.execution.context import ExecutionContext
from miros.execution.plugins.base import CommandPlugin


class APICommandPlugin(CommandPlugin):
    """Executes requests against external API integration adapters."""

    name = "api"
    priority = 80

    def can_handle(self, intent: Intent) -> bool:
        return intent.category == IntentCategory.API

    def handle(self, intent: Intent, context: ExecutionContext) -> CommandResult:
        response = context.external_api_client.request(
            action=intent.action,
            params=intent.entities,
        )
        return CommandResult(
            success=True,
            message=response.get("message", "API request completed."),
            payload=response,
        )
