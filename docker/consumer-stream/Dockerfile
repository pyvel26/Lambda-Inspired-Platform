FROM python:3.11-slim

WORKDIR /app

COPY docker/consumer-stream/requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get \
install -y procps

COPY utils.py .
COPY docker/consumer-stream/consumer.py .

CMD ["python", "consumer.py"]

