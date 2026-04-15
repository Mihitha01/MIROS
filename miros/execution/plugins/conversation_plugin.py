"""Plugin handling conversational requests via LLM abstraction."""

from __future__ import annotations

from miros.core.models import CommandResult, Intent, IntentCategory
from miros.execution.context import ExecutionContext
from miros.execution.plugins.base import CommandPlugin


class ConversationPlugin(CommandPlugin):
    """Fallback conversational plugin backed by the configured LLM provider."""

    name = "conversation"
    priority = 10

    def can_handle(self, intent: Intent) -> bool:
        return intent.category in {IntentCategory.CONVERSATION, IntentCategory.UNKNOWN}

    def handle(self, intent: Intent, context: ExecutionContext) -> CommandResult:
        history = context.memory_store.get_recent_interactions(limit=8)
        reply = context.llm_provider.generate_reply(
            prompt=intent.raw_text,
            conversation_history=history,
        )
        return CommandResult(
            success=True,
            message=reply,
            payload={"provider": context.llm_provider.name},
        )
