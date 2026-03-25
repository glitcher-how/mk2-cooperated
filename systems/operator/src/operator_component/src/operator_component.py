"""
OperatorComponent — заглушка для бизнес-действий оператора.

Содержит stubs для межсистемных действий:
- отправка заказа в НУС
- запрос доступных дронов у drone_port
- регистрация дрона в ОРВД
- подбор дрона и отправка в агрегатор
- покупка страхового полиса у страховой

Важно: это заглушки. В ответах возвращается только то, что было бы отправлено.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from broker.system_bus import SystemBus
from sdk.base_component import BaseComponent

from systems.operator.src.operator_component.topics import ComponentTopics, OperatorActions


class OperatorComponent(BaseComponent):
    def __init__(
        self,
        component_id: str,
        bus: SystemBus,
        topic: str = ComponentTopics.OPERATOR_COMPONENT,
    ):
        super().__init__(
            component_id=component_id,
            component_type="operator",
            topic=topic,
            bus=bus,
        )

    def _register_handlers(self):
        self.register_handler(OperatorActions.SEND_ORDER_TO_NUS, self._send_order_to_nus)
        self.register_handler(OperatorActions.REQUEST_AVAILABLE_DRONES, self._request_available_drones)
        self.register_handler(OperatorActions.REGISTER_DRONE_IN_ORVD, self._register_drone_in_orvd)
        self.register_handler(
            OperatorActions.SELECT_DRONE_AND_SEND_TO_AGGREGATOR,
            self._select_drone_and_send_to_aggregator,
        )
        self.register_handler(OperatorActions.BUY_INSURANCE_POLICY, self._buy_insurance_policy)

    def _send_order_to_nus(self, message: Dict[str, Any]) -> Dict[str, Any]:
        payload = message.get("payload", {}) or {}
        order = {
            "order_id": payload.get("order_id", ""),
            "pickup": payload.get("pickup", ""),
            "dropoff": payload.get("dropoff", ""),
            "weight_kg": payload.get("weight_kg", 0),
        }
        return {
            "ok": True,
            "stub": True,
            "target_system": "nus",
            "action": "receive_order",
            "order": order,
        }

    def _request_available_drones(self, message: Dict[str, Any]) -> Dict[str, Any]:
        payload = message.get("payload", {}) or {}
        return {
            "ok": True,
            "stub": True,
            "target_system": "drone_port",
            "action": "get_available_drones",
            "criteria": {
                "min_payload_kg": payload.get("min_payload_kg"),
                "min_range_km": payload.get("min_range_km"),
            },
            "drones": [],
        }

    def _register_drone_in_orvd(self, message: Dict[str, Any]) -> Dict[str, Any]:
        payload = message.get("payload", {}) or {}
        return {
            "ok": True,
            "stub": True,
            "target_system": "orvd",
            "action": "register_drone",
            "drone": {
                "drone_id": payload.get("drone_id", ""),
                "model": payload.get("model", ""),
            },
        }

    def _select_drone_and_send_to_aggregator(self, message: Dict[str, Any]) -> Dict[str, Any]:
        payload = message.get("payload", {}) or {}
        order = payload.get("order") or {}
        selected = payload.get("selected_drone_id") or ""
        return {
            "ok": True,
            "stub": True,
            "target_system": "aggregator",
            "action": "assign_drone",
            "order": {
                "order_id": order.get("order_id", ""),
                "pickup": order.get("pickup", ""),
                "dropoff": order.get("dropoff", ""),
            },
            "selected_drone_id": selected,
        }

    def _buy_insurance_policy(self, message: Dict[str, Any]) -> Dict[str, Any]:
        payload = message.get("payload", {}) or {}
        return {
            "ok": True,
            "stub": True,
            "target_system": "insurer",
            "action": "buy_policy",
            "policy": {
                "drone_id": payload.get("drone_id", ""),
                "coverage_amount": payload.get("coverage_amount", 0),
                "valid_to": payload.get("valid_to", ""),
            },
        }

