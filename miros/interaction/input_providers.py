"""Input providers for text and speech."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover - optional dependency can fail at import time.
    sr = None


class BaseInputProvider(ABC):
    """Contract for user input providers."""

    @abstractmethod
    def capture(self) -> str:
        """Capture a single user utterance."""


class TextInputProvider(BaseInputProvider):
    """CLI text input provider."""

    def __init__(self, prompt: str = "You > ") -> None:
        self.prompt = prompt

    def capture(self) -> str:
        return input(self.prompt).strip()


class SpeechInputProvider(BaseInputProvider):
    """Speech-to-text input provider using SpeechRecognition."""

    def __init__(self, timeout: int = 5, phrase_time_limit: int = 10) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit
        self.available = sr is not None
        self._recognizer = sr.Recognizer() if self.available else None

    def capture(self) -> str:
        if not self.available:
            raise RuntimeError("SpeechRecognition is not available in this environment.")

        assert self._recognizer is not None
        with sr.Microphone() as source:
            self.logger.info("Listening for voice input...")
            self._recognizer.adjust_for_ambient_noise(source, duration=0.4)
            audio = self._recognizer.listen(
                source,
                timeout=self.timeout,
                phrase_time_limit=self.phrase_time_limit,
            )

        text = self._recognizer.recognize_google(audio)
        self.logger.info("Voice input recognized: %s", text)
        return text.strip()


class HybridInputProvider(BaseInputProvider):
    """Input provider that supports text, voice, and auto fallback modes."""

    def __init__(self, mode: str = "auto") -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.mode = mode.lower()
        self.text_input = TextInputProvider()
        self.speech_input = SpeechInputProvider()

    def capture(self) -> str:
        if self.mode == "text":
            return self.text_input.capture()

        if self.mode == "voice":
            try:
                return self.speech_input.capture()
            except Exception as exc:
                self.logger.warning(
                    "Voice mode failed (%s). Falling back to text mode.", exc
                )
                return self.text_input.capture()

        try:
            return self.speech_input.capture()
        except Exception:
            return self.text_input.capture()
