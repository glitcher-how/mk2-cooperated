# Интерфейсы gateway

| Action | Вход | Типы | Ограничения | Результат | Коды ошибок |
|---|---|---|---|---|---|
| `register_drone` | `payload.drone_id`, `payload.model`, `payload.capabilities` | `str`, `str`, `dict` | `drone_id` обязателен | ответ компонента | `400` — неизвестный action |
| `request_available_drones` | `payload.budget` | `int` | `budget >= 0` | список доступных дронов | `400` — invalid payload |
| `buy_insurance_policy` | `payload.order_id`, `payload.drone_id`, `payload.coverage_amount` | `str`, `str`, `int` | `coverage_amount > 0` | страховой полис | `504` — timeout |
