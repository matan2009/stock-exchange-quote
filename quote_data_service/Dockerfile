FROM python:3.8-slim

WORKDIR /app

COPY quote_data_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY quote_data_service ./quote_data_service
COPY api ./api
COPY logger ./logger

CMD ["uvicorn", "quote_data_service.app:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]