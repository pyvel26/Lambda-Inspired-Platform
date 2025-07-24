import json
import random
from datetime import datetime
from kafka import KafkaProducer
from utils import get_logger

logger = get_logger("stream_producer")

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def generate_transaction_id():
    return f"TXN-LIVE-{datetime.now().strftime('%Y%m%d%H%M%S%f')}-{random.randint(1000, 9999)}"


def generate_fake_transaction():
    transaction_types = ['purchase', 'withdrawal', 'transfer', 'refund', 'deposit']
    categories = ['grocery', 'gas', 'restaurant', 'retail', 'electronics', 'pharmacy', 'coffee', 'entertainment']

    return {
        "transaction_id": generate_transaction_id(),
        "account_id": f"ACC-{random.randint(100000, 999999)}",
        "transaction_type": random.choice(transaction_types),
        "amount": round(random.uniform(10.00, 500.00), 2),
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "merchant_category": random.choice(categories),
        "location": "Nashville TN",
        "card_present": True,
        "risk_score": round(random.uniform(0.01, 0.9), 2)
    }


def main():
    try:
        while True:
            transaction = generate_fake_transaction()
            producer.send('transactions', transaction)
            producer.flush()
            logger.info(f"Sent transaction: {transaction['transaction_id']}")
    except KeyboardInterrupt:
        logger.info("Stream manually stopped.")
    except Exception as e:
        logger.error(f"Producer error: {e}")
    finally:
        producer.close()
        logger.info("Producer connection closed.")


if __name__ == "__main__":
    main()
