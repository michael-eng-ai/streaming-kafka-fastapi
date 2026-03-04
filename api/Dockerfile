FROM python:3.10-slim

WORKDIR /app

# Install dependencies (only what's needed for the FastAPI)
COPY requirements.txt .
RUN pip install --no-cache-dir fastapi uvicorn redis pydantic

COPY api/ .

# Expose the API port
EXPOSE 8000

# Run the Uvicorn ASGI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
