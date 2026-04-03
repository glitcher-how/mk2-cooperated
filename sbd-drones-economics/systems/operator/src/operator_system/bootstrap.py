"""Bootstrap helpers for the operator system."""

from __future__ import annotations

from typing import Any

from broker.system_bus import SystemBus
from operator_component.operator_component import OperatorComponent
from operator_component.topics import ExternalTopics
from operator_gateway.gateway import OperatorGateway


def register_demo_external_services(bus: SystemBus) -> None:
    """Register local stub handlers for external integrations."""

    def insurer_handler(message: dict[str, Any]) -> dict[str, Any]:
        """Return a deterministic insurance policy payload."""
        drone_id = message.get("payload", {}).get("drone_id", "unknown")
        return {
            "success": True,
            "payload": {
                "policy_id": f"POL-{drone_id}",
                "status": "active",
            },
        }

    def orvd_handler(message: dict[str, Any]) -> dict[str, Any]:
        """Return a deterministic ORVD registration payload."""
        drone_id = message.get("payload", {}).get("drone_id", "unknown")
        return {
            "success": True,
            "payload": {
                "registry_id": f"ORVD-{drone_id}",
                "status": "registered",
            },
        }

    bus.register_request_handler(ExternalTopics.INSURER, insurer_handler)
    bus.register_request_handler(ExternalTopics.ORVD, orvd_handler)


def build_operator_system(bus: SystemBus | None = None) -> tuple[SystemBus, OperatorGateway, OperatorComponent]:
    """Create gateway and component instances connected to a common bus."""
    local_bus = bus or SystemBus()
    register_demo_external_services(local_bus)
    component = OperatorComponent(component_id="operator_component", bus=local_bus)
    gateway = OperatorGateway(system_id="operator", bus=local_bus)
    component.start()
    gateway.run_forever()
    return local_bus, gateway, component
