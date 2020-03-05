FROM rabbitmq:3-management

RUN apt-get update && apt-get install -y python python-pip

# install the RabbitMQ python client
RUN pip install pika

COPY receive.py .

#ENTRYPOINT ["python", "receive.py"] 
ENTRYPOINT ["/bin/bash"]
