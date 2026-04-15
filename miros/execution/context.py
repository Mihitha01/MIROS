"""Shared execution context passed to plugins."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from miros.core.config import MirosConfig
from miros.execution.system_actions import SystemActionExecutor
from miros.execution.web_actions import WebActionExecutor
from miros.integration.external_api import ExternalAPIClient
from miros.integration.llm.base import LLMProvider
from miros.memory.store import MemoryStore


@dataclass
class ExecutionContext:
    """State and services required by execution plugins."""

    config: MirosConfig
    memory_store: MemoryStore
    llm_provider: LLMProvider
    external_api_client: ExternalAPIClient
    system_executor: SystemActionExecutor
    web_executor: WebActionExecutor
    logger: logging.Logger
