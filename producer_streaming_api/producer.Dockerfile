FROM python:3.11-slim

WORKDIR /app

COPY producer_streaming_api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY producer_streaming_api/producer_api.py .

CMD ["uvicorn", "producer_api:app", "--host", "--port", "8000"]