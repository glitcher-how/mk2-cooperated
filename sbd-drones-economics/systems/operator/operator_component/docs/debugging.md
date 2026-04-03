# Отладка operator_component

1. Запустить `make test` в директории сервиса.
2. Проверить содержимое `self._drones` в отладчике после вызова `register_drone`.
3. Для трассировки внешних вызовов подменять `bus.request` через `MagicMock`.
