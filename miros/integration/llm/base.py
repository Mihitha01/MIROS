"""Base contract for pluggable language model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    """Abstract language model provider."""

    name: str = "base"

    @abstractmethod
    def generate_reply(
        self,
        prompt: str,
        conversation_history: list[dict[str, Any]],
    ) -> str:
        """Generate an assistant reply for user prompt and context."""
