"""High-level multimodal interface orchestration."""

from __future__ import annotations

from miros.interaction.input_providers import HybridInputProvider
from miros.interaction.output_providers import OutputManager


class MultimodalInterface:
    """Unified interface for capturing input and delivering responses."""

    def __init__(self, input_mode: str = "auto", enable_tts: bool = True) -> None:
        self.input_provider = HybridInputProvider(mode=input_mode)
        self.output_manager = OutputManager(enable_tts=enable_tts)

    def listen(self) -> str:
        """Capture user input from the active channel."""
        return self.input_provider.capture()

    def respond(self, message: str) -> None:
        """Emit assistant response to active output channels."""
        self.output_manager.respond(message)
