FROM python:3.11-slim

WORKDIR /app

COPY producer_streaming_api/requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update && apt_get \

install -y curl

COPY . .

CMD ["python", "producer_streaming_api/producer_api.py"]
