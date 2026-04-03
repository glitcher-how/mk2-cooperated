"""Unit tests for the operator gateway."""

from unittest.mock import MagicMock

from operator_gateway.gateway import OperatorGateway
from operator_gateway.topics import ComponentTopics, GatewayActions, SystemTopics


def test_gateway_routes_actions() -> None:
    """Gateway should expose the expected topic and routing table."""
    bus = MagicMock()
    gateway = OperatorGateway(system_id="operator", bus=bus, health_port=None)
    assert gateway.topic == SystemTopics.OPERATOR
    assert gateway.ACTION_ROUTING[GatewayActions.REGISTER_DRONE] == ComponentTopics.OPERATOR_COMPONENT
    assert gateway.ACTION_ROUTING[GatewayActions.BUY_INSURANCE_POLICY] == ComponentTopics.OPERATOR_COMPONENT
