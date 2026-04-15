"""Plugin handling local system and filesystem commands."""

from __future__ import annotations

from miros.core.models import CommandResult, Intent, IntentCategory
from miros.execution.context import ExecutionContext
from miros.execution.plugins.base import CommandPlugin


class SystemCommandPlugin(CommandPlugin):
    """Handles system actions routed from intent classification."""

    name = "system"
    priority = 100

    def can_handle(self, intent: Intent) -> bool:
        return intent.category == IntentCategory.SYSTEM

    def handle(self, intent: Intent, context: ExecutionContext) -> CommandResult:
        if intent.action == "open_app":
            result = context.system_executor.open_app(intent.entities["app"])
            return CommandResult(success=True, message="Opening application.", payload=result)

        if intent.action == "list_files":
            result = context.system_executor.list_files(intent.entities.get("path"))
            entries = ", ".join(item["name"] for item in result["entries"][:10])
            preview = entries if entries else "No entries found"
            return CommandResult(
                success=True,
                message=f"Directory snapshot: {preview}",
                payload=result,
            )

        if intent.action == "read_file":
            result = context.system_executor.read_file(intent.entities["path"])
            suffix = " (truncated)" if result["truncated"] else ""
            return CommandResult(
                success=True,
                message=f"Contents of {result['path']}{suffix}:\n{result['content']}",
                payload=result,
            )

        if intent.action == "create_file":
            result = context.system_executor.create_file(
                path=intent.entities["path"],
                content=intent.entities["content"],
            )
            return CommandResult(
                success=True,
                message=f"Created file at {result['path']}.",
                payload=result,
            )

        return CommandResult(
            success=False,
            message="System command recognized but action is not implemented.",
            error=f"Unknown action: {intent.action}",
        )
