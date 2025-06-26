FROM python:3.11-slim

WORKDIR /app

COPY batch_processor/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY processor.py .

CMD ["python", "processor.py"]
