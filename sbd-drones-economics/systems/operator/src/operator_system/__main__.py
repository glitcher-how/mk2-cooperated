"""Executable bootstrap for the operator system."""

from __future__ import annotations

import time

from operator_system.bootstrap import build_operator_system


def main() -> None:
    """Start all local parts of the operator system."""
    build_operator_system()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
