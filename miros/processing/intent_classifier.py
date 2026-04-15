"""Rule-based intent classifier for MIROS commands and conversation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Pattern

from miros.core.models import Intent, IntentCategory


@dataclass(frozen=True)
class PatternRule:
    """A regex rule mapped to an intent category and action."""

    category: IntentCategory
    action: str
    pattern: Pattern[str]
    confidence: float


class IntentClassifier:
    """Classifies free-form text into structured intents."""

    def __init__(self) -> None:
        self.rules: list[PatternRule] = [
            PatternRule(
                category=IntentCategory.SYSTEM,
                action="open_app",
                pattern=re.compile(r"^(?:open|launch)\s+(?P<app>.+)$", re.IGNORECASE),
                confidence=0.95,
            ),
            PatternRule(
                category=IntentCategory.SYSTEM,
                action="list_files",
                pattern=re.compile(
                    r"^(?:list|show)\s+(?:files|directory|folder)(?:\s+in\s+(?P<path>.+))?$",
                    re.IGNORECASE,
                ),
                confidence=0.9,
            ),
            PatternRule(
                category=IntentCategory.SYSTEM,
                action="read_file",
                pattern=re.compile(
                    r"^(?:read|show)\s+file\s+(?P<path>.+)$", re.IGNORECASE
                ),
                confidence=0.92,
            ),
            PatternRule(
                category=IntentCategory.SYSTEM,
                action="create_file",
                pattern=re.compile(
                    r"^create\s+file\s+(?P<path>\S+)\s+with\s+(?P<content>.+)$",
                    re.IGNORECASE,
                ),
                confidence=0.87,
            ),
            PatternRule(
                category=IntentCategory.WEB,
                action="web_search",
                pattern=re.compile(
                    r"^(?:search\s+(?:the\s+)?web\s+for|google)\s+(?P<query>.+)$",
                    re.IGNORECASE,
                ),
                confidence=0.91,
            ),
            PatternRule(
                category=IntentCategory.WEB,
                action="open_url",
                pattern=re.compile(
                    r"^(?:open\s+(?:url|website)|browse)\s+(?P<url>.+)$",
                    re.IGNORECASE,
                ),
                confidence=0.9,
            ),
            PatternRule(
                category=IntentCategory.API,
                action="weather_lookup",
                pattern=re.compile(
                    r"^(?:what(?:'s|\s+is)\s+the\s+weather\s+(?:in\s+)?|get\s+weather\s+(?:for\s+)?)"
                    r"(?P<location>.+)$",
                    re.IGNORECASE,
                ),
                confidence=0.86,
            ),
            PatternRule(
                category=IntentCategory.API,
                action="external_api_request",
                pattern=re.compile(
                    r"^(?:api\s+request|fetch\s+api)\s+(?P<resource>.+)$",
                    re.IGNORECASE,
                ),
                confidence=0.8,
            ),
        ]

    def classify(self, text: str) -> Intent:
        """Return the best intent match for a user utterance."""
        cleaned = text.strip()
        if not cleaned:
            return Intent(
                category=IntentCategory.UNKNOWN,
                action="empty_input",
                confidence=1.0,
                raw_text=text,
            )

        for rule in self.rules:
            match = rule.pattern.match(cleaned)
            if match:
                entities = {k: v for k, v in match.groupdict().items() if v}
                return Intent(
                    category=rule.category,
                    action=rule.action,
                    entities=entities,
                    confidence=rule.confidence,
                    raw_text=text,
                )

        return Intent(
            category=IntentCategory.CONVERSATION,
            action="chat",
            entities={},
            confidence=0.35,
            raw_text=text,
        )
