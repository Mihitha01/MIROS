"""Domain models shared across MIROS layers."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class IntentCategory(str, Enum):
    """High-level intent categories understood by MIROS."""

    SYSTEM = "system"
    WEB = "web"
    API = "api"
    CONVERSATION = "conversation"
    UNKNOWN = "unknown"


@dataclass
class Intent:
    """Structured representation of user intent."""

    category: IntentCategory
    action: str
    entities: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    raw_text: str = ""


@dataclass
class CommandResult:
    """Result object returned by execution plugins."""

    success: bool
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
