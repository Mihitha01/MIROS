"""Registry and dispatcher for command plugins."""

from __future__ import annotations

import logging

from miros.core.models import CommandResult, Intent
from miros.execution.context import ExecutionContext
from miros.execution.plugins.base import CommandPlugin


class CommandRegistry:
    """Maintains plugins and dispatches intents to the correct handler."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._plugins: list[CommandPlugin] = []

    def register(self, plugin: CommandPlugin) -> None:
        self._plugins.append(plugin)
        self._plugins.sort(key=lambda p: p.priority, reverse=True)
        self.logger.info("Registered plugin: %s", plugin.name)

    def dispatch(self, intent: Intent, context: ExecutionContext) -> CommandResult:
        for plugin in self._plugins:
            if plugin.can_handle(intent):
                try:
                    return plugin.handle(intent, context)
                except Exception as exc:
                    self.logger.exception("Plugin %s failed", plugin.name)
                    return CommandResult(
                        success=False,
                        message="Execution failed due to an internal error.",
                        error=str(exc),
                    )

        return CommandResult(
            success=False,
            message="No plugin could handle this request.",
            error=f"Unhandled intent category: {intent.category.value}",
        )
