from kafka import KafkaProducer
from dotenv import load_dotenv
import os
import json
import traceback
from datetime import datetime, UTC

print("KAFKA PRODUCER INITIALIZATION")
load_dotenv()

BOOTSTRAP_SERVER = os.getenv("AIVEN_KAFKA_BOOTSTRAP_SERVER")
USERNAME = os.getenv("AIVEN_KAFKA_USERNAME")
PASSWORD = os.getenv("AIVEN_KAFKA_PASSWORD")
TOPIC = os.getenv("AIVEN_KAFKA_TOPIC")

print(f"[{datetime.now(UTC)}] Bootstrap Server : {BOOTSTRAP_SERVER}")
print(f"[{datetime.now(UTC)}] Username         : {USERNAME}")
print(f"[{datetime.now(UTC)}] Topic            : {TOPIC}")

if not BOOTSTRAP_SERVER:
    raise ValueError("AIVEN_KAFKA_BOOTSTRAP_SERVER is missing")

if not USERNAME:
    raise ValueError("AIVEN_KAFKA_USERNAME is missing")

if not PASSWORD:
    raise ValueError("AIVEN_KAFKA_PASSWORD is missing")

if not TOPIC:
    raise ValueError("AIVEN_KAFKA_TOPIC is missing")

print(f"[{datetime.now(UTC)}] Creating Kafka Producer...")

try:

    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVER,
        security_protocol="SASL_SSL",
        sasl_mechanism="SCRAM-SHA-256",
        sasl_plain_username=USERNAME,
        sasl_plain_password=PASSWORD,
        ssl_cafile="ca.pem",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    print(f"[{datetime.now(UTC)}] Kafka Producer Created Successfully")

except Exception as e:

    print(f"[{datetime.now(UTC)}] FAILED TO CREATE PRODUCER")
    print(repr(e))
    traceback.print_exc()
    raise

print("PRODUCER READY")


def send_transaction(transaction):

    print(f"[{datetime.now(UTC)}] Preparing transaction")

    try:

        print(
            f"[{datetime.now(UTC)}] "
            f"TXN_ID={transaction.get('transaction_id')}"
        )

        print(
            f"[{datetime.now(UTC)}] "
            f"Sending to Topic={TOPIC}"
        )

        future = producer.send(
            TOPIC,
            value=transaction
        )

        print(
            f"[{datetime.now(UTC)}] "
            f"Message submitted to producer buffer"
        )

        print(
            f"[{datetime.now(UTC)}] "
            f"Waiting for Kafka acknowledgement..."
        )

        record_metadata = future.get(timeout=30)

        print(
            f"[{datetime.now(UTC)}] "
            f"KAFKA ACK RECEIVED"
        )

        print(
            f"[{datetime.now(UTC)}] "
            f"Topic={record_metadata.topic}"
        )

        print(
            f"[{datetime.now(UTC)}] "
            f"Partition={record_metadata.partition}"
        )

        print(
            f"[{datetime.now(UTC)}] "
            f"Offset={record_metadata.offset}"
        )

        producer.flush()

        print(
            f"[{datetime.now(UTC)}] "
            f"Producer Flush Completed"
        )

        print(
            f"[{datetime.now(UTC)}] "
            f"Transaction Successfully Published"
        )

    except Exception as e:

        print("=" * 80)
        print("KAFKA SEND FAILED")
        print("=" * 80)

        print(f"Exception Type : {type(e).__name__}")
        print(f"Exception      : {repr(e)}")

        traceback.print_exc()

        raise