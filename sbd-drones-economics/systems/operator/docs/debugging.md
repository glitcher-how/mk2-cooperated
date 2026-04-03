# Отладка системы operator

1. Запустить `make tests-all` в корне репозитория.
2. Проверить маршрутизацию gateway через `systems/operator/gateway/tests`.
3. Проверить бизнес-логику через `systems/operator/operator_component/tests`.
4. Для сквозной отладки запустить `PYTHONPATH=... python -m operator_system` и отправлять сообщения через `SystemBus` в интерактивной сессии.
