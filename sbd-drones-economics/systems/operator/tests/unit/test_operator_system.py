"""Unit tests for the operator system bootstrap."""

from operator_system.bootstrap import build_operator_system


def test_build_operator_system_registers_handlers() -> None:
    """Bootstrap should return initialized gateway and component instances."""
    bus, gateway, component = build_operator_system()
    assert gateway.topic == "systems.operator"
    assert component.topic == "components.operator"
    assert bus.request("systems.insurer", {"payload": {"drone_id": "d1"}})["success"] is True
