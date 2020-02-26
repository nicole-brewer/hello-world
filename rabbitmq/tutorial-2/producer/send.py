#!/usr/bin/env python
import pika
import sys
## RabbitMQ is a message broker that accepts and forwards messages


# establish connection with RabbitMQ server (broker)
# in this example, the localhost is acting as the producer, consumer, and broker.
# If this app were a consumer or producer (or both) on a different machine than the broker, we'd attempt to connect to the IP of the broker node instead

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create a new queue that manages tasks
# durable=True makes the queue persistent so that if RabbitMQ crashes, the queue does not
channel.queue_declare(queue='task_queue', durable=True)

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






