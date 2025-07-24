import pandas as pd
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

try:
    cur = conn
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
    job_id VARCHAR(50) NOT NULL,
    transaction_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    merchant_category VARCHAR(50),
    location VARCHAR(100),
    card_present BOOLEAN NOT NULL,
    risk_score DECIMAL(3,2) NOT NULL
    )
    """)
    conn.commit()
    cur = conn.cursor()
except Exception as e:
    print(f"The following error occurred: {e}")



for message in consumer:
    cur = None  # Initialize to avoid scope issues
    try:
        cur = conn.cursor()
        data = message.value  # Already a dict
        cur.execute("""
            INSERT INTO transactions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (transaction_id) DO NOTHING
        """, (
            data["job_id"],
            data["transaction_id"],
            data["account_id"],
            data["transaction_type"],
            data["amount"],
            data["timestamp"],
            data["merchant_category"],
            data["location"],
            data["card_present"],
            data["risk_score"]
        ))

        conn.commit()
        print(f"✅ Inserted: {data['transaction_id']}")

    except psycopg2.errors.DataError as e:
        print(f"📊 Data format error: {e}")
        conn.rollback()

    except psycopg2.OperationalError as e:
        print(f"🔌 Database connection error: {e}")
        conn.rollback()

    except KeyError as e:
        print(f"🔑 Missing field in message: {e}")
        # No rollback needed - no DB operation happened

    except json.JSONDecodeError as e:
        print(f"📄 Invalid JSON in message: {e}")
        # No rollback needed - no DB operation happened

    finally:
        if cur:
            cur.close()
