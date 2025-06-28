import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
bootstrap_servers=['kafka:9092'],
value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def generate_fake_transaction():
    transaction_types = ['purchase', 'withdrawal', 'transfer', 'refund', 'deposit']
    categories = ['grocery', 'gas', 'restaurant', 'retail', 'electronics', 'pharmacy', 'coffee', 'entertainment']

    return {
        "transaction_id": f"TXN-LIVE-{random.randint(1000, 9999)}",
        "account_id": f"ACC-{random.randint(1000, 9999)}",
        "type": random.choice(transaction_types),
        "amount": round(random.uniform(10.00, 500.00), 2),
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "category": random.choice(categories),
        "location": "Nashville TN",
        "valid": True,
        "fraud_probability": round(random.uniform(0.01, 0.9), 2)
    }


# Send to Kafka
while True:
    # Send structured JSON
    producer.send('transactions', generate_fake_transaction())
    producer.flush()
    time.sleep(2)  # Generate every 2 seconds

