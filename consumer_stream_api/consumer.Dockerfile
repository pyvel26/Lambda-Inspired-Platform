FROM python:3.11-slim

WORKDIR /app

COPY consumer_stream_api/requirements.txt .

RUN pip install -r requirements.txt

COPY consumer_stream_api/consumer_api.py .

CMD ["uvicorn", "consumer_api:app", "--host", "0.0.0.0", "--port", "8000"]

