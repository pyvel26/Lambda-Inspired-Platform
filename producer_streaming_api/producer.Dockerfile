FROM python:3.11-slim

WORKDIR /app

COPY producer_streaming_api/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "producer_streaming_api/producer_api.py"]
