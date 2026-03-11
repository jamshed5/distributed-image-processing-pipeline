import json
import os
from confluent_kafka import Producer, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
from dotenv import load_dotenv

load_dotenv()

BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS")
TOPIC_NAME = os.getenv("TOPIC_NAME")
IMAGE_DIR = os.getenv("IMAGE_DIR")


def create_topic():
    """Create the Kafka/Redpanda topic if it doesn't exist"""
    admin = AdminClient({"bootstrap.servers": BOOTSTRAP_SERVERS})
    topic = NewTopic(TOPIC_NAME, num_partitions=1, replication_factor=1)

    fs = admin.create_topics([topic])
    for t, f in fs.items():
        try:
            f.result()
            print(f"Topic '{t}' created successfully")
        except KafkaException as e:
            print(f"Topic '{t}' already exists or creation failed: {e}")


def delivery_report(err, msg):
    """Called once for each produced message to indicate delivery result"""
    if err is not None:
        print(f"Delivery failed for {msg.key().decode()}: {err}")
    else:
        print(
            f"Delivered -> {msg.key().decode()} | "
            f"Partition: {msg.partition()} | Offset: {msg.offset()}"
        )


def send_images():
    """Send file paths of images in IMAGE_DIR to Kafka"""
    producer = Producer({"bootstrap.servers": BOOTSTRAP_SERVERS})

    for file in os.listdir(IMAGE_DIR):
        path = os.path.join(IMAGE_DIR, file)
        if not os.path.isfile(path):
            continue

        # Send the file path instead of encoding the image
        message = {
            "filename": file,
            "path": path  # local file path
        }

        print(f"Sending image path: {file}")
        producer.produce(
            TOPIC_NAME,
            key=file.encode(),
            value=json.dumps(message),
            callback=delivery_report
        )

        # Trigger delivery report callbacks
        producer.poll(0.1)

    # Ensure all messages are delivered before exiting
    producer.flush()
    print("All image paths sent successfully")


if __name__ == "__main__":
    create_topic()
    send_images()