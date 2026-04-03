"""Base abstractions for message-driven business components."""

from __future__ import annotations

from typing import Any, Callable, Dict, Mapping

Message = Dict[str, Any]
MessageHandler = Callable[[Message], Message]


class BaseComponent:
    """Base class for synchronous message-driven components."""

    def __init__(self, component_id: str, topic: str, bus: Any) -> None:
        """Store component metadata and transport dependency."""
        self.component_id = component_id
        self.topic = topic
        self.bus = bus
        self._handlers: dict[str, MessageHandler] = {}

    def register_handler(self, action: str, handler: MessageHandler) -> None:
        """Register a function for a specific business action."""
        self._handlers[action] = handler

    def handle_message(self, message: Mapping[str, Any]) -> Message:
        """Dispatch an incoming message to a registered handler."""
        action = str(message.get("action", "")).strip()
        if not action:
            raise ValueError("action is required")
        if action not in self._handlers:
            raise ValueError(f"unsupported action: {action}")
        return self._handlers[action](dict(message))

    def start(self) -> None:
        """Register the component as a request handler in the bus."""
        self.bus.register_request_handler(self.topic, self.handle_message)
