import pandas as pd
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Read CSV with pandas
df = pd.read_csv("data/financial_transactions.csv")

# Send each row as JSON
for _, row in df.iterrows():
    row_dict = row.to_dict()
    producer.send('transactions', row_dict)
producer.flush()
