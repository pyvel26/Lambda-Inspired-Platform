import pandas as pd
from typing import List, Dict, Tuple
from kafka import KafkaProducer
import json
import os


producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)



data = "data/financial_transactions.csv"

with open(data, 'r') as file:
    for line in file:
        producer.send('transactions', line.encode('utf-8'))
producer.flush()



