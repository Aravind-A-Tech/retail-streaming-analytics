from kafka import KafkaProducer
from dotenv import load_dotenv
import os
import json

load_dotenv()

producer = KafkaProducer(
    bootstrap_servers=os.getenv("AIVEN_KAFKA_BOOTSTRAP_SERVER"),
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-256",
    sasl_plain_username=os.getenv("AIVEN_KAFKA_USERNAME"),
    sasl_plain_password=os.getenv("AIVEN_KAFKA_PASSWORD"),
    ssl_cafile="ca.pem",
    api_version=(3, 7, 0),   # <-- add this line
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_transaction(transaction):
    future = producer.send(
        os.getenv("AIVEN_KAFKA_TOPIC"),
        value=transaction
    )

    record_metadata = future.get(timeout=10)

    print(
        f"Sent to topic={record_metadata.topic}, "
        f"partition={record_metadata.partition}, "
        f"offset={record_metadata.offset}"
    )

    producer.flush()