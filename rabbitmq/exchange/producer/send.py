#!/usr/local/bin/python3
import pika
import sys

# establish connection with RabbitMQ server (broker)
# in this example, the localhost is acting as the producer, consumer, and broker.
# If this app were a consumer or producer (or both) on a different machine than the broker, we'd attempt to connect to the IP of the broker node instead
credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-server', 5672, "/", credentials))
channel = connection.channel()

# create a new queue that manages tasks
# durable=True makes the queue persistent so that if RabbitMQ crashes, the queue does not
# channel.queue_declare(queue='task_queue', durable=True)
# We no longer have to declare the queue because it is in our config

# receive message and pass it on with it's message property
message = ' '.join(sys.argv[1:]) or 'Hello world!'

# messages aren't direclty sent directly to the queue, but rather they go through exchanges where they are forwarded to the appropriate queue
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties( delivery_mode=2, )) # makes the message persistent so that if RabbitMQ crashes, the message doesn't)
print(" [x] Sent %r" % message)


# flush network buffers
connection.close()






