from unittest.mock import MagicMock

from systems.operator.src.gateway.src.gateway import OperatorGateway
from systems.operator.src.gateway.topics import ComponentTopics, GatewayActions, SystemTopics
from systems.operator.src.operator_component.src.operator_component import OperatorComponent
from systems.operator.src.operator_component.topics import OperatorActions


def test_operator_component_handles_send_order_to_nus():
    bus = MagicMock()
    comp = OperatorComponent(component_id="operator_component", bus=bus)
    msg = {
        "action": OperatorActions.SEND_ORDER_TO_NUS,
        "payload": {"order_id": "O-1", "pickup": "A", "dropoff": "B", "weight_kg": 2},
    }
    result = comp._handlers[OperatorActions.SEND_ORDER_TO_NUS](msg)
    assert result["ok"] is True
    assert result["stub"] is True
    assert result["target_system"] == "nus"
    assert result["order"]["order_id"] == "O-1"


def test_operator_component_handles_request_available_drones():
    bus = MagicMock()
    comp = OperatorComponent(component_id="operator_component", bus=bus)
    msg = {"action": OperatorActions.REQUEST_AVAILABLE_DRONES, "payload": {"min_range_km": 10}}
    result = comp._handlers[OperatorActions.REQUEST_AVAILABLE_DRONES](msg)
    assert result["target_system"] == "drone_port"
    assert isinstance(result["drones"], list)


def test_operator_gateway_routes_actions_to_component():
    bus = MagicMock()
    gw = OperatorGateway(system_id="operator", bus=bus, health_port=None)

    assert gw.topic == SystemTopics.OPERATOR
    assert gw.ACTION_ROUTING[GatewayActions.SEND_ORDER_TO_NUS] == ComponentTopics.OPERATOR_COMPONENT
    assert gw.ACTION_ROUTING[GatewayActions.BUY_INSURANCE_POLICY] == ComponentTopics.OPERATOR_COMPONENT

