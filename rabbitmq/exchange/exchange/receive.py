#!/usr/bin/env python
import pika
import time

# connect to the broker as before
credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-server', 5672, "/", credentials))
channel = connection.channel()

# To receive a message, we must subscribe a callback function to the queue that is called
# every time we receive a message
# We do the subscribing via the on_message_callback parameter on initialization of the 
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # pretend to do some work 
    time.sleep(body.count(b'.'))
    print(" [x] Done")


# We want the queue to dispatch only as the receiving queues are emptied, instead of all the tasks evenly to each queue immediately
# at the time of their receipt. 
channel.basic_qos(prefetch_count=1)

# create consumer and subscribe the callback function
# We set auto_ack to True so that when the message has been received and processed, RabbitMQ receives a message
# that it is safe to delete. 
# If the consumer dies (and it's connection is lost) and it hasn't sent an ack, RabbitMQ passes on the work to another consumer.
# Manual message acknowledgements are the default, but here we have it turned on to auto
channel.basic_consume(
    queue='task_queue', on_message_callback=callback, auto_ack=True)

# The consumer will run continuously waiting for deliveries until interrupted via <Ctrl-C>
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
