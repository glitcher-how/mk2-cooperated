FROM python:3.13-slim

WORKDIR /app

COPY config/requirements.txt /app/config/requirements.txt
RUN pip install -r /app/config/requirements.txt --no-cache-dir

COPY . /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "systems.operator.src.gateway"]

