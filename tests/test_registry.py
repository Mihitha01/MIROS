from pathlib import Path

from miros.core.config import MirosConfig
from miros.core.models import Intent, IntentCategory
from miros.execution.context import ExecutionContext
from miros.execution.plugins.conversation_plugin import ConversationPlugin
from miros.execution.registry import CommandRegistry
from miros.execution.system_actions import SystemActionExecutor
from miros.execution.web_actions import WebActionExecutor
from miros.integration.external_api import MockExternalAPIClient
from miros.integration.llm.mock_provider import MockLLMProvider
from miros.memory.store import MemoryStore


def test_registry_dispatches_to_conversation_plugin(tmp_path: Path) -> None:
    config = MirosConfig.from_env(workspace_root=tmp_path)
    memory_store = MemoryStore(config.memory_db_path)

    context = ExecutionContext(
        config=config,
        memory_store=memory_store,
        llm_provider=MockLLMProvider(),
        external_api_client=MockExternalAPIClient(),
        system_executor=SystemActionExecutor(config.workspace_root),
        web_executor=WebActionExecutor(config.web_search_endpoint),
        logger=__import__("logging").getLogger("test"),
    )

    registry = CommandRegistry()
    registry.register(ConversationPlugin())

    intent = Intent(
        category=IntentCategory.CONVERSATION,
        action="chat",
        raw_text="hello miros",
    )

    result = registry.dispatch(intent, context)

    assert result.success is True
    assert "MIROS" in result.message.upper()
