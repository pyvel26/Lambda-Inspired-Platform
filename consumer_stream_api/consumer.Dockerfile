FROM python:3.11-slim

WORKDIR /app

COPY consumer_stream_api/requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get \
install -y procps

COPY consumer_stream_api/consumer_api.py .

CMD ["python", "consumer_stream_api/consumer_api.py"]

