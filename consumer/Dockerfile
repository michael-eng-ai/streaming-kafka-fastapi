FROM python:3.10-slim

WORKDIR /app

# Install dependencies (only what's needed for consumer)
COPY requirements.txt .
RUN pip install --no-cache-dir confluent-kafka redis

COPY consumer/ .

CMD ["python", "main.py"]
