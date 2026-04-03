"""Local in-memory implementation of a synchronous request bus."""

from __future__ import annotations

from typing import Any, Callable, Dict

MessageHandler = Callable[[dict[str, Any]], dict[str, Any]]


class SystemBus:
    """Simple synchronous bus for local runs and automated tests."""

    def __init__(self) -> None:
        """Create an empty registry of request handlers."""
        self._handlers: dict[str, MessageHandler] = {}

    def register_request_handler(self, topic: str, handler: MessageHandler) -> None:
        """Bind a handler to a topic name."""
        self._handlers[topic] = handler

    def request(
        self,
        topic: str,
        message: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Synchronously deliver a message to a handler."""
        del timeout
        if topic not in self._handlers:
            raise KeyError(f"handler for topic {topic!r} is not registered")
        return self._handlers[topic](message)

    def reset(self) -> None:
        """Remove all registered handlers."""
        self._handlers.clear()
