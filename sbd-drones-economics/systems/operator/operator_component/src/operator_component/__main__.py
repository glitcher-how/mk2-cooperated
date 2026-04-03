"""Entry point for the operator business component."""

from __future__ import annotations

import os
import time

from broker.bus_factory import create_system_bus
from operator_component.operator_component import OperatorComponent


def main() -> None:
    """Start the component and keep the process alive."""
    component_id = os.environ.get("COMPONENT_ID", "operator_component")
    bus = create_system_bus(client_id=component_id)
    component = OperatorComponent(component_id=component_id, bus=bus)
    component.start()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
