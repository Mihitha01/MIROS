"""SQLite-backed conversation memory store."""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from miros.core.models import CommandResult, Intent


class MemoryStore:
    """Persists assistant interactions and provides recent context retrieval."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._lock = threading.Lock()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_text TEXT NOT NULL,
                    assistant_text TEXT NOT NULL,
                    intent_category TEXT NOT NULL,
                    intent_action TEXT NOT NULL,
                    metadata_json TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def record_interaction(
        self,
        user_text: str,
        assistant_text: str,
        intent: Intent,
        result: CommandResult,
    ) -> None:
        """Store a user/assistant turn with intent and execution metadata."""
        metadata = {
            "confidence": intent.confidence,
            "entities": intent.entities,
            "payload": result.payload,
            "success": result.success,
            "error": result.error,
        }
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")

        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO interactions (
                    timestamp,
                    user_text,
                    assistant_text,
                    intent_category,
                    intent_action,
                    metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    now,
                    user_text,
                    assistant_text,
                    intent.category.value,
                    intent.action,
                    json.dumps(metadata),
                ),
            )
            conn.commit()

    def get_recent_interactions(self, limit: int = 8) -> list[dict[str, Any]]:
        """Return recent interactions in chronological order for context injection."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT timestamp, user_text, assistant_text, intent_category, intent_action, metadata_json
                FROM interactions
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        interactions: list[dict[str, Any]] = []
        for row in reversed(rows):
            interactions.append(
                {
                    "timestamp": row["timestamp"],
                    "user_text": row["user_text"],
                    "assistant_text": row["assistant_text"],
                    "intent_category": row["intent_category"],
                    "intent_action": row["intent_action"],
                    "metadata": json.loads(row["metadata_json"]),
                }
            )
        return interactions
