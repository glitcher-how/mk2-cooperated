"""Unit tests for shared SDK abstractions."""

from broker.system_bus import SystemBus
from sdk_core.base_component import BaseComponent
from sdk_core.base_gateway import BaseGateway


def test_base_component_dispatches_registered_handler() -> None:
    """Ensure BaseComponent dispatches a supported action."""
    bus = SystemBus()
    component = BaseComponent(component_id="demo", topic="components.demo", bus=bus)
    component.register_handler("ping", lambda message: {"pong": message["payload"]})
    assert component.handle_message({"action": "ping", "payload": 1}) == {"pong": 1}


def test_base_gateway_proxies_to_component() -> None:
    """Ensure BaseGateway sends a request to the resolved component."""
    bus = SystemBus()
    bus.register_request_handler("components.demo", lambda message: {"ok": message["action"]})

    class DemoGateway(BaseGateway):
        """Test implementation of BaseGateway."""

        ACTION_ROUTING = {"ping": "components.demo"}

    gateway = DemoGateway(
        system_id="demo",
        system_type="demo",
        topic="systems.demo",
        bus=bus,
    )
    assert gateway.handle_message({"action": "ping"}) == {"ok": "ping"}
