"""Configuration management for MIROS."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _to_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class MirosConfig:
    """Application settings loaded from environment variables."""

    app_name: str
    input_mode: str
    enable_tts: bool
    enable_stt: bool
    llm_provider: str
    log_level: str
    workspace_root: Path
    data_dir: Path
    memory_db_path: Path
    web_search_endpoint: str

    @classmethod
    def from_env(cls, workspace_root: Path) -> "MirosConfig":
        """Build config from .env and process environment."""
        load_dotenv()

        root = workspace_root.resolve()
        data_dir = Path(os.getenv("MIROS_DATA_DIR", str(root / "data"))).resolve()
        data_dir.mkdir(parents=True, exist_ok=True)

        memory_path = Path(
            os.getenv("MIROS_MEMORY_DB", str(data_dir / "miros_memory.db"))
        ).resolve()

        return cls(
            app_name=os.getenv("MIROS_APP_NAME", "MIROS"),
            input_mode=os.getenv("MIROS_INPUT_MODE", "auto").lower(),
            enable_tts=_to_bool(os.getenv("MIROS_ENABLE_TTS"), default=True),
            enable_stt=_to_bool(os.getenv("MIROS_ENABLE_STT"), default=True),
            llm_provider=os.getenv("MIROS_LLM_PROVIDER", "mock").lower(),
            log_level=os.getenv("MIROS_LOG_LEVEL", "INFO").upper(),
            workspace_root=root,
            data_dir=data_dir,
            memory_db_path=memory_path,
            web_search_endpoint=os.getenv(
                "MIROS_WEB_SEARCH_ENDPOINT",
                "https://duckduckgo.com/?q={query}",
            ),
        )
