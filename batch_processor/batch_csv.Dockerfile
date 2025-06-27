FROM python:3.11-slim

WORKDIR /app

COPY batch_processor/requirements.txt .

RUN pip install -r requirements.txt

COPY batch_processor/processor.py .

CMD ["python", "processor.py"]