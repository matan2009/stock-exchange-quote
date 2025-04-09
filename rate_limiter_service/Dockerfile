FROM python:3.8-slim

WORKDIR /app

COPY rate_limiter_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rate_limiter_service ./rate_limiter_service
COPY api ./api
COPY logger ./logger

CMD ["uvicorn", "rate_limiter_service.app:app", "--host", "0.0.0.0", "--port", "8000",  "--workers", "4"]