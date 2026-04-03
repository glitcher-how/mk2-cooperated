"""Entry point for the operator gateway service."""

from __future__ import annotations

import os
import time

from broker.bus_factory import create_system_bus
from operator_gateway.gateway import OperatorGateway


def main() -> None:
    """Start the gateway and keep the process alive."""
    system_id = os.environ.get("SYSTEM_ID", "operator")
    health_port = int(os.environ.get("HEALTH_PORT", "0")) or None
    bus = create_system_bus(client_id=system_id)
    gateway = OperatorGateway(system_id=system_id, bus=bus, health_port=health_port)
    gateway.run_forever()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
