# Интерфейсы operator_component

| Action | Вход | Типы | Ограничения | Выход | Коды ошибок |
|---|---|---|---|---|---|
| `register_drone` | `drone_id`, `model`, `capabilities` | `str`, `str`, `dict` | `drone_id` обязателен | `status`, `drone_id` | `400` — `drone_id is required` |
| `request_available_drones` | `budget` | `int` | `budget >= 0` | `drones[]` | `400` — invalid budget |
| `select_drone_and_send_to_aggregator` | `selected_drone_id`, `order_id` | `str`, `str` | дрон должен существовать и быть доступным | `status`, `drone_id`, `order_id` | `404` — drone not found, `409` — not available |
| `buy_insurance_policy` | `order_id`, `drone_id`, `coverage_amount` | `str`, `str`, `int` | `coverage_amount > 0` | `status`, `policy` | `504` — insurer timeout, `502` — insurer error |
| `register_drone_in_orvd` | `drone_id`, `model` | `str`, `str` | `drone_id` обязателен | `status`, `orvd_response` | `504` — ORVD timeout, `502` — ORVD error |
| `send_order_to_nus` | `order_id` | `str` | заглушка | `status`, `note` | не используется |
