# Drone Operator System

Event-driven microservice for managing UAV (drone) operations. Built as part of a multi-team distributed systems course (PIKS-MK, SPbGU, Spring 2026).

The operator system receives delivery orders from an aggregator, coordinates with a drone port, registers missions with air traffic control (ORVD), dispatches orders to the ground control station (GCS), and purchases insurance policies — all via an asynchronous message bus.

## Architecture

```
Aggregator ──► [ Kafka / MQTT ] ──► OperatorGateway ──► OperatorComponent
                                                               │
                               ┌───────────────────────────────┤
                               ▼           ▼           ▼       ▼
                             [GCS]   [DronePort]   [ORVD]  [Insurer]
```

**OperatorGateway** — entry point, routes incoming actions to internal components.

**OperatorComponent** — business logic: selects drones, registers missions, buys insurance.

**Broker SDK** — abstraction layer supporting both Kafka and MQTT backends, switchable via env var.

## Tech Stack

- Python 3.11
- Kafka (`kafka-python`) / MQTT (`paho-mqtt`)
- Docker / Docker Compose
- pytest

## Getting Started

### Requirements

- Docker + Docker Compose
- Python 3.11+
- pipenv

### Install dependencies

```bash
cd config
pipenv install
```

### Run with Docker

```bash
cd systems/operator
make docker-up
```

### Stop

```bash
make docker-down
```

### Run tests

```bash
cd systems/operator
make unit-test
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `BROKER_TYPE` | `kafka` | Message broker: `kafka` or `mqtt` |
| `KAFKA_BOOTSTRAP_SERVERS` | `kafka:29092` | Kafka broker address |
| `SYSTEM_ID` | `operator` | System identifier |
| `SYSTEM_NAMESPACE` | — | Topic namespace |

## Message Topics

| System | Topic | Direction |
|---|---|---|
| Aggregator | `v1.aggregator_insurer.local.operator.requests` | Incoming orders |
| Aggregator | `v1.aggregator_insurer.local.operator.responses` | Price offers / results |
| GCS | `v1.gcs.1.orchestrator` | Dispatch order to drone |
| DronePort | `v1.drone_port.1.orchestrator` | Request available drones |
| ORVD | `v1.ORVD.ORVD001.main` | Register drone and mission |
| Insurer | `v1.Insurer.1.insurer-service.requests` | Purchase insurance policy |

## Project Context

This system was developed as part of a larger multi-team simulation involving:
- Aggregator / Insurer
- Drone Operator (this repo)
- Ground Control Station (GCS)
- Drone Port
- Air Traffic Control (ORVD)

Each team implemented their own system independently, communicating only through the shared message bus contract.

## Author

Alexander Kovalev
