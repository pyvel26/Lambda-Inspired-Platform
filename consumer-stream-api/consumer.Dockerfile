FROM python:3.11-slim

WORKDIR /app

COPY services/api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY api.py .

CMD ["uvicorn", "api:app", "--host", "--port", "8000"]
