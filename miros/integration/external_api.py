"""Abstractions for external API integrations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ExternalAPIClient(ABC):
    """Contract for external API adapters."""

    @abstractmethod
    def request(self, action: str, params: dict[str, Any]) -> dict[str, Any]:
        """Execute an action against an external API and return normalized payload."""


class MockExternalAPIClient(ExternalAPIClient):
    """Mock API adapter enabling integration testing without network dependencies."""

    def request(self, action: str, params: dict[str, Any]) -> dict[str, Any]:
        if action == "weather_lookup":
            location = params.get("location", "your area")
            return {
                "action": action,
                "location": location,
                "temperature_c": 23,
                "condition": "Partly cloudy",
                "message": f"Weather for {location}: 23C, partly cloudy.",
            }

        if action == "external_api_request":
            resource = params.get("resource", "unknown")
            return {
                "action": action,
                "resource": resource,
                "status": "mocked",
                "message": f"Mock API response retrieved for resource '{resource}'.",
            }

        return {
            "action": action,
            "status": "unsupported",
            "message": "Mock API adapter received unsupported action.",
        }
