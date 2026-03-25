# Система эксплуатанта — Team M2

Система эксплуатанта беспилотных авиационных систем. Курс ПИКС-МК, весна 2026, команда M2.

## Описание

Система принимает заказы от агрегатора, подбирает дроны через дронопорт, регистрирует миссии в ОРВД, взаимодействует с НУС и страховой компанией.

## Архитектура

```
systems/operator/
├── src/
│   ├── gateway/            — точка входа, роутинг входящих запросов
│   └── operator_component/ — бизнес-логика
└── tests/                  — unit-тесты
```

Система построена на SDK с шиной сообщений (Kafka / MQTT).

## Взаимодействие с другими системами

| Система | Топик | Действие |
|---|---|---|
| Агрегатор (входящие) | `v1.aggregator_insurer.local.operator.requests` | Получение заказов |
| Агрегатор (исходящие) | `v1.aggregator_insurer.local.operator.responses` | Оферта цены, результат выполнения |
| НУС / GCS | `v1.gcs.1.orchestrator` | Постановка задачи дрону |
| Дронопорт | `v1.drone_port.1.orchestrator` | Запрос доступных дронов |
| ОРВД | `v1.ORVD.ORVD001.main` | Регистрация дрона и миссии |
| Страховая | `v1.Insurer.1.insurer-service.requests` | Покупка страхового полиса |

## Запуск

### Требования

- Docker + Docker Compose
- Python 3.11+
- pipenv

### Установка зависимостей

```bash
cd config
pipenv install
```

### Запуск через Docker

```bash
cd systems/operator
make docker-up
```

### Остановка

```bash
make docker-down
```

### Тесты

```bash
cd systems/operator
make unit-test
```

## Переменные окружения

| Переменная | По умолчанию | Описание |
|---|---|---|
| `BROKER_TYPE` | `kafka` | Тип брокера: `kafka` или `mqtt` |
| `KAFKA_BOOTSTRAP_SERVERS` | `kafka:29092` | Адрес Kafka |
| `SYSTEM_ID` | `operator` | Идентификатор системы |
| `SYSTEM_NAMESPACE` | — | Пространство имён топиков |
