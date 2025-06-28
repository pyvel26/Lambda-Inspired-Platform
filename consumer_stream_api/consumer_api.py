import pandas as pd
import psycopg2
import json
import os
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

host = os.getenv('DB_HOST')
password = os.getenv('DB_PASSWORD')
user = os.getenv('DB_USER')
database = os.getenv('DB_NAME')
port = os.getenv('DB_PORT')

conn = psycopg2.connect(host=host,
                        database=database,
                        port=port,
                        user=user,
                        password=password)

cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
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

for message in consumer:
    data = message.value  # Already a dict
    print(f"Received data: {data}")
    print(f"Data type: {type(data)}")
    cur.execute("""
        INSERT INTO transactions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
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
cur.close()
conn.close()
