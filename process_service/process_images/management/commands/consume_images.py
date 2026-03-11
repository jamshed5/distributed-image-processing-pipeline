import json
import time
from django.core.management.base import BaseCommand
from confluent_kafka import Consumer, KafkaError
from process_images.tasks import process_image  # Celery task
import os
from dotenv import load_dotenv

load_dotenv()

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC_NAME = os.getenv("KAFKA_TOPIC_NAME")
GROUP_ID = os.getenv("KAFKA_CONSUMER_GROUP")

BATCH_SIZE = int(os.getenv("KAFKA_BATCH_SIZE", 5))
BATCH_TIMEOUT = int(os.getenv("KAFKA_BATCH_TIMEOUT", 5)) #5 seconds


class Command(BaseCommand):
    help = 'Consume image paths from Redpanda and push to Celery for batch processing'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Redpanda image consumer...")

        consumer = Consumer({
            "bootstrap.servers": BOOTSTRAP_SERVERS,
            "group.id": GROUP_ID,
            "auto.offset.reset":os.getenv("KAFKA_AUTO_OFFSET_RESET", "earliest"),
            "enable.auto.commit": False,  # Manual commit for reliability
        })
        consumer.subscribe([TOPIC_NAME])
        self.stdout.write(f"Subscribed to topic: {TOPIC_NAME}")

        batch = []
        last_flush_time = time.time()

        try:
            while True:
                msg = consumer.poll(timeout=1.0)
                current_time = time.time()

                # Flush batch if timeout passed
                if batch and (current_time - last_flush_time) >= BATCH_TIMEOUT:
                    process_image.delay(batch)
                    self.stdout.write(f"Flushed {len(batch)} image paths to Celery (timeout)")
                    consumer.commit(asynchronous=False)
                    batch = []
                    last_flush_time = current_time

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() != KafkaError._PARTITION_EOF:
                        self.stderr.write(f"Kafka error: {msg.error()}")
                    continue

                # Decode JSON safely
                try:
                    message = json.loads(msg.value().decode())
                    filename = message["filename"]
                    path = message["path"]  # read path instead of base64
                    batch.append((path, filename))
                except (json.JSONDecodeError, KeyError) as e:
                    self.stderr.write(f"Skipping invalid message: {e}")
                    continue

                # Send batch if full
                if len(batch) >= BATCH_SIZE:
                    process_image.delay(batch)
                    self.stdout.write(f"Sent batch of {len(batch)} image paths to Celery")
                    consumer.commit(asynchronous=False)
                    batch = []
                    last_flush_time = current_time

        except KeyboardInterrupt:
            self.stdout.write("Stopping consumer...")

        finally:
            # Flush remaining images
            if batch:
                process_image.delay(batch)
                consumer.commit(asynchronous=False)
                self.stdout.write(f"Flushed remaining {len(batch)} image paths to Celery")
            consumer.close()
            self.stdout.write("Consumer closed")