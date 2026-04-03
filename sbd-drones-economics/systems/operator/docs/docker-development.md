# Разработка системы operator в Docker

```bash
docker compose build
docker compose up operator_system
```

Для режима раздельных контейнеров предусмотрен профиль `split`, но он требует реального межпроцессного брокера сообщений.
