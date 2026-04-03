# Интерфейсы sdk-core

| Сущность | Тип данных | Ограничения | Ошибки |
|---|---|---|---|
| `SystemBus.request(topic, message, timeout)` | `str`, `dict`, `float | None` | topic не должен быть пустым | `KeyError` при отсутствии обработчика |
| `BaseComponent.handle_message(message)` | `dict` | должен содержать поле `action` | `ValueError` для неизвестного action |
| `BaseGateway.handle_message(message)` | `dict` | action должен быть описан в `ACTION_ROUTING` | `ValueError` для неизвестного action |
