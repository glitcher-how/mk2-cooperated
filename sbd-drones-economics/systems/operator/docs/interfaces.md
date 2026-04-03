# Интерфейсы системы operator

## Внешний интерфейс gateway

| Action | Входные данные | Типы | Ограничения | Успешный ответ | Коды ошибок |
|---|---|---|---|---|---|
| `register_drone` | `drone_id`, `model`, `capabilities` | `str`, `str`, `dict` | `drone_id` обязателен | `status=registered` | `400` — invalid payload |
| `request_available_drones` | `budget` | `int` | `budget >= 0` | список дронов | `400` — invalid payload |
| `buy_insurance_policy` | `order_id`, `drone_id`, `coverage_amount` | `str`, `str`, `int` | `coverage_amount > 0` | страховой полис | `504` — insurer timeout |
| `register_drone_in_orvd` | `drone_id`, `model` | `str`, `str` | `drone_id` обязателен | статус регистрации | `504` — ORVD timeout |

## Внутренний интерфейс компонента

Компонент принимает те же `action`, но обрабатывает их на топике `components.operator`.
