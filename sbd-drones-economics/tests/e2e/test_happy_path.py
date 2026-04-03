"""End-to-end happy-path tests for the repository demo flow."""

from operator_gateway.topics import GatewayActions
from operator_system.bootstrap import build_operator_system


def test_full_happy_path() -> None:
    """Register a drone, insure it and register it in ORVD through the gateway."""
    bus, _, _ = build_operator_system()
    bus.request(
        "systems.operator",
        {
            "action": GatewayActions.REGISTER_DRONE,
            "payload": {"drone_id": "e2e-1", "model": "Demo", "capabilities": {}},
        },
    )
    insurance = bus.request(
        "systems.operator",
        {
            "action": GatewayActions.BUY_INSURANCE_POLICY,
            "payload": {
                "order_id": "ord-1",
                "drone_id": "e2e-1",
                "coverage_amount": 2000,
            },
        },
    )
    orvd = bus.request(
        "systems.operator",
        {
            "action": GatewayActions.REGISTER_DRONE_IN_ORVD,
            "payload": {"drone_id": "e2e-1", "model": "Demo"},
        },
    )
    assert insurance["status"] == "insured"
    assert orvd["status"] == "registered_in_orvd"
