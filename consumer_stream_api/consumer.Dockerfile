FROM python:3.11-slim

WORKDIR /app

COPY consumer_stream_api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY consumer_stream_api/consumer_api.py .

CMD ["python", "consumer_api.py"]
