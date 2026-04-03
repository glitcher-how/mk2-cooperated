"""Module tests for the complete operator system flow."""

from operator_gateway.topics import GatewayActions
from operator_system.bootstrap import build_operator_system


def test_register_and_list_available_drones() -> None:
    """A drone registered through the gateway should appear in the availability list."""
    bus, _, _ = build_operator_system()
    bus.request(
        "systems.operator",
        {
            "action": GatewayActions.REGISTER_DRONE,
            "payload": {"drone_id": "d1", "model": "Agro-X", "capabilities": {}},
        },
    )
    result = bus.request(
        "systems.operator",
        {
            "action": GatewayActions.REQUEST_AVAILABLE_DRONES,
            "payload": {"budget": 1500},
        },
    )
    assert result["drones"][0]["drone_id"] == "d1"
