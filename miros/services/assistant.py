"""Top-level assistant orchestration service."""

from __future__ import annotations

import logging

from miros.core.config import MirosConfig
from miros.core.models import Intent
from miros.execution.context import ExecutionContext
from miros.execution.plugins.api_plugin import APICommandPlugin
from miros.execution.plugins.conversation_plugin import ConversationPlugin
from miros.execution.plugins.system_plugin import SystemCommandPlugin
from miros.execution.plugins.web_plugin import WebCommandPlugin
from miros.execution.registry import CommandRegistry
from miros.execution.system_actions import SystemActionExecutor
from miros.execution.web_actions import WebActionExecutor
from miros.integration.external_api import MockExternalAPIClient
from miros.integration.llm.mock_provider import MockLLMProvider
from miros.interaction.interface import MultimodalInterface
from miros.memory.store import MemoryStore
from miros.processing.intent_classifier import IntentClassifier
from miros.processing.intent_router import IntentRouter


class MirosAssistantService:
    """Coordinates all layers of MIROS in a runtime loop."""

    def __init__(self, config: MirosConfig) -> None:
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

        self.interface = MultimodalInterface(
            input_mode=config.input_mode,
            enable_tts=config.enable_tts,
        )

        self.intent_classifier = IntentClassifier()
        self.intent_router = IntentRouter()

        self.memory_store = MemoryStore(config.memory_db_path)
        self.registry = CommandRegistry()

        context = ExecutionContext(
            config=config,
            memory_store=self.memory_store,
            llm_provider=MockLLMProvider(),
            external_api_client=MockExternalAPIClient(),
            system_executor=SystemActionExecutor(config.workspace_root),
            web_executor=WebActionExecutor(config.web_search_endpoint),
            logger=self.logger,
        )
        self.execution_context = context

        self.registry.register(SystemCommandPlugin())
        self.registry.register(WebCommandPlugin())
        self.registry.register(APICommandPlugin())
        self.registry.register(ConversationPlugin())

    def process_text(self, user_text: str) -> str:
        """Process one user prompt end-to-end and return assistant response."""
        intent: Intent = self.intent_classifier.classify(user_text)
        domain = self.intent_router.route(intent)

        self.logger.info(
            "Intent classified | category=%s action=%s confidence=%.2f domain=%s",
            intent.category.value,
            intent.action,
            intent.confidence,
            domain,
        )

        result = self.registry.dispatch(intent, self.execution_context)
        response = result.message if result.success else f"Request failed: {result.error}"

        self.memory_store.record_interaction(
            user_text=user_text,
            assistant_text=response,
            intent=intent,
            result=result,
        )

        return response

    def run_once(self, prompt: str) -> str:
        """Run a single-turn interaction for scripting or testing."""
        response = self.process_text(prompt)
        self.interface.respond(response)
        return response

    def run_forever(self) -> None:
        """Run interactive loop until user exits."""
        self.interface.respond(
            "MIROS initialized. Say or type a request. Use 'exit' to shut down."
        )

        while True:
            try:
                user_text = self.interface.listen()
            except KeyboardInterrupt:
                self.interface.respond("Shutdown requested. MIROS going offline.")
                break
            except Exception as exc:
                self.logger.exception("Input layer failed")
                self.interface.respond(f"Input error: {exc}")
                continue

            if not user_text:
                continue

            if user_text.strip().lower() in {"exit", "quit", "shutdown"}:
                self.interface.respond("Shutting down MIROS.")
                break

            response = self.process_text(user_text)
            self.interface.respond(response)
