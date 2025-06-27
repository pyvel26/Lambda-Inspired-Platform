FROM python:3.11-slim

WORKDIR /app

COPY producer_streaming_api/requirements.txt .

RUN pip install -r requirements.txt

COPY producer_streaming_api/producer_api.py .

CMD ["uvicorn", "producer_api:app", "--host", "0.0.0.0", "--port", "8000"]
