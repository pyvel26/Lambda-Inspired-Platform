FROM python:3.11-slim

WORKDIR /app

COPY batch_processor/requirements.txt .


RUN pip install -r requirements.txt
RUN apt-get update

COPY batch_processor/processor.py .

CMD ["python", "batch_processor/processor.py"]