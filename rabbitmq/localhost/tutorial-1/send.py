#!/usr/bin/env python
import pika

## RabbitMQ is a message broker that accepts and forwards messages


# establish connection with RabbitMQ server (broker)
# in this example, the localhost is acting as the producer, consumer, and broker.
# If this app were a consumer or producer (or both) on a different machine than the broker, we'd attempt to connect to the IP of the broker node instead

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create a new queue called hello
channel.queue_declare(queue='hello')

# messages aren't direclty sent directly to the queue, but rather they go through exchanges where they are forwarded to the appropriate queue
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")


# flush network buffers
connection.close()






