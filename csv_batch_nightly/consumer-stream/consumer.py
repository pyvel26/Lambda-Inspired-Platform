import json
from kafka import KafkaConsumer
from utils import get_db_connection, get_logger



logger = get_logger("consumer")


def create_consumer() -> KafkaConsumer:
    """
    Create and return a Kafka consumer configured to read JSON messages from the 'transactions' topic.

    Returns:
        KafkaConsumer: Configured consumer instance.
    """
    return KafkaConsumer(
        'transactions',
        bootstrap_servers=['kafka:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )


def process_message(cur, data: dict) -> None:
    """
    Insert a single transaction record into the 'transactions' table, skipping duplicates.

    Args:
        cur: Active database cursor.
        data (dict): Deserialized transaction message.
    """
    data["ingestion_type"] = data.get("ingestion_type", "STREAM")

    cur.execute("""
        INSERT INTO transactions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (transaction_id) DO NOTHING
    """, (
        data.get("job_id"),
        data["transaction_id"],
        data["account_id"],
        data["transaction_type"],
        data["amount"],
        data["timestamp"],
        data["merchant_category"],
        data["location"],
        data["card_present"],
        data["risk_score"],
        data["ingestion_type"]
    ))


def main() -> None:
    """
    Consume transaction messages from Kafka and insert them into the PostgreSQL database.
    Handles connection, deserialization, conflict avoidance, and rollback on error.
    """
    consumer = create_consumer()
    conn = get_db_connection()

    for message in consumer:
        try:
            cur = conn.cursor()
            process_message(cur, message.value)
            conn.commit()
            logger.info(f"Inserted: {message.value['transaction_id']}")
        except Exception as e:
            logger.info(f"Error processing message: {e}")
            conn.rollback()
        finally:
            cur.close()


if __name__ == "__main__":
    main()
