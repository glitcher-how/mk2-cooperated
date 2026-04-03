"""Unit tests for the operator business component."""

from unittest.mock import MagicMock

from operator_component.operator_component import OperatorComponent
from operator_component.topics import OperatorActions


def test_register_drone() -> None:
    """A valid drone should be registered in memory."""
    bus = MagicMock()
    component = OperatorComponent(component_id="operator_component", bus=bus)
    result = component.handle_message(
        {
            "action": OperatorActions.REGISTER_DRONE,
            "payload": {
                "drone_id": "d1",
                "model": "Agrodron",
                "capabilities": {"type": "agrodron"},
            },
        }
    )
    assert result["status"] == "registered"
    assert "d1" in component._drones


def test_request_available_drones_with_registered() -> None:
    """Only drones with available status should be returned."""
    bus = MagicMock()
    component = OperatorComponent(component_id="operator_component", bus=bus)
    component._drones["d1"] = {
        "drone_id": "d1",
        "model": "X",
        "status": "available",
        "operator_id": "op",
    }
    component._drones["d2"] = {
        "drone_id": "d2",
        "model": "Y",
        "status": "assigned",
        "operator_id": "op",
    }
    result = component.handle_message(
        {
            "action": OperatorActions.REQUEST_AVAILABLE_DRONES,
            "payload": {"budget": 500},
        }
    )
    assert len(result["drones"]) == 1
    assert result["drones"][0]["drone_id"] == "d1"


def test_buy_insurance_calls_insurer() -> None:
    """The component should proxy insurance requests to the external topic."""
    bus = MagicMock()
    bus.request.return_value = {
        "success": True,
        "payload": {"policy_id": "pol1", "status": "active"},
    }
    component = OperatorComponent(component_id="operator_component", bus=bus)
    result = component.handle_message(
        {
            "action": OperatorActions.BUY_INSURANCE_POLICY,
            "payload": {
                "drone_id": "d1",
                "coverage_amount": 5000,
                "order_id": "o1",
            },
        }
    )
    assert result["status"] == "insured"
    assert result["policy"]["policy_id"] == "pol1"
