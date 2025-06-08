# kafka/kafka_producer.py
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(email, name, similarity, company):
    data = {
        "email": email,
        "name": name,
        "similarity": similarity,
        "company": company
    }
    producer.send('resume_evaluation_results', value=data)
    producer.flush()
