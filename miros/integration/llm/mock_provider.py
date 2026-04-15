"""Mock LLM provider for local development and deterministic behavior."""

from __future__ import annotations

from typing import Any

from miros.integration.llm.base import LLMProvider


class MockLLMProvider(LLMProvider):
    """Simple rules-backed reply generator used as default provider."""

    name = "mock"

    def generate_reply(
        self,
        prompt: str,
        conversation_history: list[dict[str, Any]],
    ) -> str:
        lowered = prompt.strip().lower()

        if any(token in lowered for token in {"hello", "hi", "hey"}):
            return "Hello. MIROS online and ready."

        if "who are you" in lowered or "your name" in lowered:
            return "I am MIROS, your modular local AI operating layer."

        if "what can you do" in lowered:
            return (
                "I can classify intents, execute system commands, trigger web actions, "
                "perform mock external API calls, and keep short-term interaction memory."
            )

        if conversation_history:
            latest = conversation_history[-1].get("user_text", "")
            return (
                "I understand. Based on recent context, you asked about "
                f"'{latest}'. How would you like to continue?"
            )

        return (
            "I processed your conversational request. "
            "To improve answer quality, plug in a production LLM provider in the integration layer."
        )
