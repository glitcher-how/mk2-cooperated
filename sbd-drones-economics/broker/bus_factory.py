"""Factory methods for creating local bus instances."""

from __future__ import annotations

from broker.system_bus import SystemBus

_GLOBAL_BUS = SystemBus()


def create_system_bus(client_id: str) -> SystemBus:
    """Return a process-wide shared bus for local development."""
    del client_id
    return _GLOBAL_BUS


def reset_system_bus() -> None:
    """Reset the shared process-wide bus instance."""
    _GLOBAL_BUS.reset()
