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
    transaction = message.value.decode('utf-8')
    row = transaction.split(',')
    cur.execute("""
    INSERT INTO transactions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()
cur.close()
conn.close()
