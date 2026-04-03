"""Module tests for the operator component with a real local bus."""

from broker.system_bus import SystemBus
from operator_component.operator_component import OperatorComponent
from operator_component.topics import ExternalTopics, OperatorActions


def test_component_handles_external_orvd_request() -> None:
    """A component should return ORVD registration data via the local bus."""
    bus = SystemBus()
    bus.register_request_handler(
        ExternalTopics.ORVD,
        lambda message: {
            "success": True,
            "payload": {"registry_id": f"ORVD-{message['payload']['drone_id']}"},
        },
    )
    component = OperatorComponent(component_id="operator_component", bus=bus)
    result = component.handle_message(
        {
            "action": OperatorActions.REGISTER_DRONE_IN_ORVD,
            "payload": {"drone_id": "d1", "model": "Agro-X"},
        }
    )
    assert result["status"] == "registered_in_orvd"
    assert result["orvd_response"]["registry_id"] == "ORVD-d1"
