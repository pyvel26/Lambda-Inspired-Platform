FROM python:3.11-slim

WORKDIR /app

COPY docker/csv-batch/requirements.txt .


RUN pip install -r requirements.txt
RUN apt-get update

COPY docker/csv-batch/processor.py .

CMD ["python", "docker/csv-batch/processor.py"]