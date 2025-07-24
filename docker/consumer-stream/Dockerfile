FROM python:3.11-slim

WORKDIR /app

COPY docker/consumer_stream/requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get \
install -y procps

COPY docker/consumer_stream/consumer.py .

CMD ["python", "docker/consumer_stream/consumer.py"]

