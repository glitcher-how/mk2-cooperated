"""Business logic of the operator component."""

from __future__ import annotations

from typing import Any

from sdk_core.base_component import BaseComponent

from operator_component.topics import ComponentTopics, ExternalTopics, OperatorActions


class OperatorComponent(BaseComponent):
    """Operator business component working through a request bus."""

    EXTERNAL_REQUEST_TIMEOUT = 5.0

    def __init__(self, component_id: str, bus: Any) -> None:
        """Initialize storage and register all supported actions."""
        super().__init__(component_id=component_id, topic=ComponentTopics.OPERATOR_COMPONENT, bus=bus)
        self._drones: dict[str, dict[str, Any]] = {}
        self.register_handler(OperatorActions.REGISTER_DRONE, self._handle_register_drone)
        self.register_handler(
            OperatorActions.REQUEST_AVAILABLE_DRONES,
            self._handle_request_available_drones,
        )
        self.register_handler(
            OperatorActions.SELECT_DRONE_AND_SEND_TO_AGGREGATOR,
            self._handle_select_drone,
        )
        self.register_handler(OperatorActions.BUY_INSURANCE_POLICY, self._handle_buy_insurance)
        self.register_handler(
            OperatorActions.REGISTER_DRONE_IN_ORVD,
            self._handle_register_in_orvd,
        )
        self.register_handler(OperatorActions.SEND_ORDER_TO_NUS, self._handle_send_to_nus)

    def _handle_register_drone(self, message: dict[str, Any]) -> dict[str, Any]:
        """Register a drone in the operator registry."""
        payload = message.get("payload", {}) or {}
        drone_id = str(payload.get("drone_id", "")).strip()
        if not drone_id:
            raise ValueError("drone_id is required")

        self._drones[drone_id] = {
            "drone_id": drone_id,
            "model": payload.get("model", ""),
            "capabilities": payload.get("capabilities", {}),
            "status": "available",
            "operator_id": self.component_id,
        }
        return {"status": "registered", "drone_id": drone_id}

    def _handle_request_available_drones(
        self,
        message: dict[str, Any],
    ) -> dict[str, Any]:
        """Return all currently available drones."""
        payload = message.get("payload", {}) or {}
        available_drones = []
        for drone in self._drones.values():
            if drone["status"] != "available":
                continue
            available_drones.append(
                {
                    "drone_id": drone["drone_id"],
                    "model": drone.get("model", ""),
                    "operator_id": drone.get("operator_id", self.component_id),
                    "price": payload.get("budget", 1000),
                }
            )
        return {"drones": available_drones}

    def _handle_select_drone(self, message: dict[str, Any]) -> dict[str, Any]:
        """Assign a selected drone to an order."""
        payload = message.get("payload", {}) or {}
        drone_id = str(payload.get("selected_drone_id", "")).strip()
        order_id = str(payload.get("order_id", "")).strip()

        drone = self._drones.get(drone_id)
        if drone is None:
            raise ValueError(f"drone {drone_id} not found")
        if drone["status"] != "available":
            raise ValueError(
                f"drone {drone_id} is not available (status: {drone['status']})"
            )

        drone["status"] = "assigned"
        drone["assigned_order"] = order_id
        return {"status": "assigned", "drone_id": drone_id, "order_id": order_id}

    def _handle_buy_insurance(self, message: dict[str, Any]) -> dict[str, Any]:
        """Purchase an insurance policy through the bus."""
        payload = message.get("payload", {}) or {}
        response = self.bus.request(
            ExternalTopics.INSURER,
            {
                "action": "purchase_policy",
                "sender": self.component_id,
                "payload": {
                    "order_id": payload.get("order_id", ""),
                    "operator_id": self.component_id,
                    "drone_id": payload.get("drone_id", ""),
                    "coverage_amount": payload.get("coverage_amount", 0),
                },
            },
            timeout=self.EXTERNAL_REQUEST_TIMEOUT,
        )
        if response is None:
            raise TimeoutError("insurer did not respond")
        if response.get("success"):
            return {"status": "insured", "policy": response.get("payload", {})}
        raise RuntimeError(f"insurance failed: {response.get('error', 'unknown')}")

    def _handle_register_in_orvd(self, message: dict[str, Any]) -> dict[str, Any]:
        """Register a drone in the ORVD registry."""
        payload = message.get("payload", {}) or {}
        drone_id = str(payload.get("drone_id", "")).strip()
        if not drone_id:
            raise ValueError("drone_id is required")

        response = self.bus.request(
            ExternalTopics.ORVD,
            {
                "action": "register_drone",
                "sender": self.component_id,
                "payload": {
                    "drone_id": drone_id,
                    "model": payload.get("model", ""),
                    "operator_id": self.component_id,
                },
            },
            timeout=self.EXTERNAL_REQUEST_TIMEOUT,
        )
        if response is None:
            raise TimeoutError("ORVD did not respond")
        if response.get("success"):
            return {
                "status": "registered_in_orvd",
                "drone_id": drone_id,
                "orvd_response": response.get("payload", {}),
            }
        raise RuntimeError(f"ORVD registration failed: {response.get('error', 'unknown')}")

    def _handle_send_to_nus(self, message: dict[str, Any]) -> dict[str, Any]:
        """Return a stub response for NUS integration."""
        payload = message.get("payload", {}) or {}
        return {
            "status": "sent_to_nus",
            "order_id": payload.get("order_id", ""),
            "note": "NUS integration pending",
        }
