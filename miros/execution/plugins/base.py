"""Plugin protocol for executable command handlers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from miros.core.models import CommandResult, Intent
from miros.execution.context import ExecutionContext


class CommandPlugin(ABC):
    """Base class for action plugins."""

    name: str = "base"
    priority: int = 0

    @abstractmethod
    def can_handle(self, intent: Intent) -> bool:
        """Return whether this plugin can handle the intent."""

    @abstractmethod
    def handle(self, intent: Intent, context: ExecutionContext) -> CommandResult:
        """Execute the intent and return a command result."""
