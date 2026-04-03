"""Operator gateway implementation."""

from __future__ import annotations

from typing import Any, Optional

from sdk_core.base_gateway import BaseGateway

from operator_gateway.topics import ComponentTopics, GatewayActions, SystemTopics


class OperatorGateway(BaseGateway):
    """Gateway that proxies external requests to the operator component."""

    ACTION_ROUTING = {
        GatewayActions.REGISTER_DRONE: ComponentTopics.OPERATOR_COMPONENT,
        GatewayActions.REQUEST_AVAILABLE_DRONES: ComponentTopics.OPERATOR_COMPONENT,
        GatewayActions.SELECT_DRONE_AND_SEND_TO_AGGREGATOR: ComponentTopics.OPERATOR_COMPONENT,
        GatewayActions.BUY_INSURANCE_POLICY: ComponentTopics.OPERATOR_COMPONENT,
        GatewayActions.REGISTER_DRONE_IN_ORVD: ComponentTopics.OPERATOR_COMPONENT,
        GatewayActions.SEND_ORDER_TO_NUS: ComponentTopics.OPERATOR_COMPONENT,
    }
    PROXY_TIMEOUT = 10.0

    def __init__(
        self,
        system_id: str,
        bus: Any,
        health_port: Optional[int] = None,
    ) -> None:
        """Initialize the gateway with routing metadata."""
        super().__init__(
            system_id=system_id,
            system_type="operator",
            topic=SystemTopics.OPERATOR,
            bus=bus,
            health_port=health_port,
        )
