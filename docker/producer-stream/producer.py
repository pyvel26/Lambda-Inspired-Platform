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
"""
Kafka producer instance configured to serialize messages as UTF-8 encoded JSON.
Connects to Kafka broker at 'kafka:9092'.
"""


def generate_transaction_id() -> str:
    """
    Generate a unique transaction ID using the current timestamp and a random 4-digit number.

    Returns:
        str: A unique transaction ID in the format 'TXN-<timestamp>-<random_int>'.
    """
    return f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S%f')}-{random.randint(1000, 9999)}"


def generate_fake_transaction() -> dict:
    """
    Generate a fake financial transaction with randomized details.

    Returns:
        dict: A dictionary containing simulated transaction data including ID, type, amount, timestamp, etc.
    """
    transaction_types = ['purchase', 'withdrawal', 'transfer', 'refund', 'deposit']
    categories = ['grocery', 'gas', 'restaurant', 'retail', 'electronics', 'pharmacy', 'coffee', 'entertainment']

    return {
        "transaction_id": f"TXN-{random.randint(10000000, 99999999)}",
        "account_id": f"ACC-{random.randint(100000, 999999)}",
        "transaction_type": random.choice(transaction_types),
        "amount": round(random.uniform(10.00, 500.00), 2),
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "merchant_category": random.choice(categories),
        "location": "Nashville TN",
        "card_present": True,
        "risk_score": round(random.uniform(0.01, 0.9), 2)
    }


def main() -> None:
    """
    Continuously generate and send fake transaction data to a Kafka topic named 'transactions'.

    Sends data every iteration until interrupted (e.g., Ctrl+C).
    Logs success and error events. Ensures the Kafka producer is properly closed on exit.
    """
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
