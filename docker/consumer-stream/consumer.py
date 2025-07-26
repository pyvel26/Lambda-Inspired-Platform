import psycopg2
import json
from utils import get_db_connection
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

conn = get_db_connection()

for message in consumer:
    try:
        cur = conn.cursor()
        data = message.value

        # Set default ingestion type for stream data
        data["ingestion_type"] = data.get("ingestion_type", "STREAM")

        cur.execute("""
            INSERT INTO transactions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (transaction_id) DO NOTHING
        """, (
            data.get("job_id"),  # Will be None for stream data
            data["transaction_id"],
            data["account_id"],
            data["transaction_type"],
            data["amount"],
            data["timestamp"],  # Fixed field name
            data["merchant_category"],
            data["location"],
            data["card_present"],
            data["risk_score"],
            data["ingestion_type"]
        ))

        conn.commit()
        print(f"Inserted: {data['transaction_id']}")

    except Exception as e:
        print(f"Error processing message: {e}")
        conn.rollback()
    finally:
        if 'cur' in locals():
            cur.close()