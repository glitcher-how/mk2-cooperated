# Разработка operator_component в Docker

```bash
docker build -f systems/operator/operator_component/dockerfile -t operator-component .
docker run --rm operator-component
```

Для полноценного межконтейнерного сценария требуется внешний брокер сообщений.
