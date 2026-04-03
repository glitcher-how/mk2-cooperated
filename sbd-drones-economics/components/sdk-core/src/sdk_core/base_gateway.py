"""Base abstractions for synchronous system gateways."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

Message = Dict[str, object]


class BaseGateway:
    """Base gateway that routes actions to internal component topics."""

    ACTION_ROUTING: dict[str, str] = {}
    PROXY_TIMEOUT = 5.0

    def __init__(
        self,
        system_id: str,
        system_type: str,
        topic: str,
        bus: Any,
        health_port: Optional[int] = None,
    ) -> None:
        """Store gateway configuration and transport dependency."""
        self.system_id = system_id
        self.system_type = system_type
        self.topic = topic
        self.bus = bus
        self.health_port = health_port

    def handle_message(self, message: Mapping[str, object]) -> Message:
        """Resolve component route and proxy the request to the bus."""
        action = str(message.get("action", "")).strip()
        if not action:
            raise ValueError("action is required")
        if action not in self.ACTION_ROUTING:
            raise ValueError(f"unsupported action: {action}")
        target_topic = self.ACTION_ROUTING[action]
        response = self.bus.request(target_topic, dict(message), timeout=self.PROXY_TIMEOUT)
        if response is None:
            raise TimeoutError(f"no response from {target_topic}")
        return response

    def run_forever(self) -> None:
        """Register the gateway in the bus."""
        self.bus.register_request_handler(self.topic, self.handle_message)
