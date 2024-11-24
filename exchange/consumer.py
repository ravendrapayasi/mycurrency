import pika
from django.conf import settings
import django
import os
import sys
import json
from .tasks import load_historical_data

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycurrency.settings')
django.setup()

def callback(ch, method, properties, body):
    #print(f"Received message: {body.decode()}")
    # Deserialize the JSON message
    message = json.loads(body)
    print(f"Received message: {message}")
    load_historical_data(message['start_date'],message['end_date'])
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE, durable=True)

    print(f"Waiting for messages from {settings.RABBITMQ_QUEUE}...")
    channel.basic_consume(queue=settings.RABBITMQ_QUEUE, on_message_callback=callback)
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
