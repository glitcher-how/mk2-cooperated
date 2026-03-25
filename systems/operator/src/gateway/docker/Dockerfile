FROM python:3.13-slim

WORKDIR /app

COPY config/Pipfile /app/config/Pipfile
COPY config/Pipfile.lock /app/config/Pipfile.lock

COPY . /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "systems.operator.src.gateway"]

