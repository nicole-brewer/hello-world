#!/usr/bin/env python
import pika
import sys

# connect to the broker as before
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.exchange_declare(exchange='direct_logs',exchange_type='direct')

# we declare a queue with a random name by using an empty stirng
# we use the exclusive flage to indicate that when the consumer connection is closed, the queue should be deleted
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue


severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" %sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='direct_logs',
            queue=queue_name,
            routing_key=severity)



# To receive a message, we must subscribe a callback function to the queue that is called
# every time we receive a message
# We do the subscribing via the on_message_callback parameter on initialization of the 
def callback(ch, method, properties, body):
    print(" [x] Received %r:%r" % (method.routing_key, body))


# create consumer and subscribe the callback function
# We set auto_ack to True so that when the message has been received and processed, RabbitMQ receives a message
# that it is safe to delete. 
# If the consumer dies (and it's connection is lost) and it hasn't sent an ack, RabbitMQ passes on the work to another consumer.
# Manual message acknowledgements are the default, but here we have it turned on to auto
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

# The consumer will run continuously waiting for deliveries until interrupted via <Ctrl-C>
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
