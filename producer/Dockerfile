FROM python:3.10-slim

WORKDIR /app

# Install dependencies (only what's needed for producer)
COPY requirements.txt .
RUN pip install --no-cache-dir confluent-kafka requests

COPY producer/ .

CMD ["python", "main.py"]
