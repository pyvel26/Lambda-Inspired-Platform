FROM python:3.11-slim

WORKDIR /app

COPY docker/producer_stream/requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get \
install -y procps

COPY docker/producer_stream/producer.py .

CMD ["python", "docker/producer_stream/producer.py"]
