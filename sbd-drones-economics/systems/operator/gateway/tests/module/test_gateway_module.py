"""Module tests for operator gateway with a local bus."""

from broker.system_bus import SystemBus
from operator_gateway.gateway import OperatorGateway
from operator_gateway.topics import GatewayActions


def test_gateway_proxies_to_registered_component() -> None:
    """Gateway should forward a request to the component topic."""
    bus = SystemBus()
    bus.register_request_handler(
        "components.operator",
        lambda message: {"forwarded_action": message["action"]},
    )
    gateway = OperatorGateway(system_id="operator", bus=bus)
    result = gateway.handle_message({"action": GatewayActions.REGISTER_DRONE, "payload": {}})
    assert result == {"forwarded_action": GatewayActions.REGISTER_DRONE}
