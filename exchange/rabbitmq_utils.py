import pika
from django.conf import settings
import json
def get_connection_and_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()
    return connection, channel

def publish_message(queue_name, message):
    connection, channel = get_connection_and_channel()
    channel.queue_declare(queue=queue_name, durable=True)  # Declare a durable queue
    serialized_message = json.dumps(message)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=serialized_message,
        properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
    )
    connection.close()
    print(f"Message sent to {queue_name}: {message}")
