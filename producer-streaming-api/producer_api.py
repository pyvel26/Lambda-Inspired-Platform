from kafka import KafkaProducer
import pandas as pd
import json, random
from datetime import datetime
from fastapi import FastAPI

producer = KafkaProducer(
bootstrap_servers=['localhost:9092'],
value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def generate_fake_transaction():
    transaction_types = ['purchase', 'withdrawal', 'transfer', 'refund', 'deposit']
    categories = ['grocery', 'gas', 'restaurant', 'retail', 'electronics', 'pharmacy', 'coffee', 'entertainment']

    transaction_type = random.choice(transaction_types)
    category = random.choice(categories)

    fake_transaction = f"TXN-LIVE-{random.randint(1000, 9999)},ACC-{random.randint(1000, 9999)},{transaction_type}," \
                       f"{random.uniform(10.00, 500.00):.2f},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}," \
                       f"{category},Nashville TN,true,{random.uniform(0.01, 0.9):.2f}"

    return fake_transaction


# Send to Kafka
fake_data = generate_fake_transaction()
producer.send('transactions', fake_data.encode('utf-8'))



@app.post("/transaction")
async def create_transaction(transaction_data: dict):
    producer.send('transactions', transaction_data)
    producer.flush()
    return {"status": "sent to kafka"}

