#!/usr/bin/env python
import pika
import sys
## RabbitMQ is a message broker that accepts and forwards messages


# establish connection with RabbitMQ server (broker)
# in this example, the localhost is acting as the producer, consumer, and broker.
# If this app were a consumer or producer (or both) on a different machine than the broker, we'd attempt to connect to the IP of the broker node instead

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# this time round we send messages to the exchange instead of directly to the queue
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')


severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

# messages aren't direclty sent directly to the queue, but rather they go through exchanges where they are forwarded to the appropriate queue
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)
print(" [x] Sent %r:%r" % (severity, message))


# flush network buffers
connection.close()






