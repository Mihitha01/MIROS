"""Output providers for text and speech."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

try:
    import pyttsx3
except Exception:  # pragma: no cover - optional dependency can fail at import time.
    pyttsx3 = None


class BaseOutputProvider(ABC):
    """Contract for response output providers."""

    @abstractmethod
    def emit(self, message: str) -> None:
        """Emit a response to the user."""


class ConsoleOutputProvider(BaseOutputProvider):
    """Simple terminal output provider."""

    def emit(self, message: str) -> None:
        print(f"MIROS > {message}")


class TTSOutputProvider(BaseOutputProvider):
    """Text-to-speech provider using pyttsx3."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.available = pyttsx3 is not None
        self._engine = pyttsx3.init() if self.available else None

    def emit(self, message: str) -> None:
        if not self.available or self._engine is None:
            raise RuntimeError("pyttsx3 is not available in this environment.")

        self._engine.say(message)
        self._engine.runAndWait()


class OutputManager:
    """Coordinates text and speech output channels."""

    def __init__(self, enable_tts: bool = True) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.console = ConsoleOutputProvider()
        self.enable_tts = enable_tts
        self.tts = TTSOutputProvider() if enable_tts else None

    def respond(self, message: str) -> None:
        self.console.emit(message)
        if self.enable_tts and self.tts is not None:
            try:
                self.tts.emit(message)
            except Exception as exc:
                self.logger.warning("TTS output failed: %s", exc)
