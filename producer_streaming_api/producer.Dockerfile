FROM python:3.11-slim

WORKDIR /app

COPY producer_streaming_api/requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get \
install -y procps

COPY producer_streaming_api/producer_api.py .

CMD ["python", "producer_streaming_api/producer_api.py"]
