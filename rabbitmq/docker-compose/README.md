# RabbitMQ from docker-compose

## Motivation

We've already seen that we can run RabbitMQ and interact with it through localhost ports. But perhaps we also want to containerize the micro-applications such as send.py, and receive.py as they begin to require more complicated builds. For this reason, we can use three docker containers. As our queueing system get's more complicated, we also might want more control of our RabbitMQ configuration. This requires the use of volumes, because configuration files have to be present **before** the image is actual built.

## The Compose File: Three Containers (services)

1. **rabbitmq-server**

   Notice that this continer is built directly from the same image we used before. And the same port mappings. There's a network definition too but well come back to those later.

   ```yaml
   version: "3" 
   services:
       rabbitmq-server:
         image: rabbitmq:3-management
         container_name: rabbitmq-server
         ports:
           - "5672:5672"
           - "15672:15672"
         volumes:
           - ./.docker/rabbitmq/etc/:/etc/rabbitmq/
           - ./.docker/rabbitmq/data/:/var/lib/rabbitmq/
           - ./.docker/rabbitmq/logs/:/var/log/rabbitmq/
           - ./definitions.json:/etc/rabbitmq/definitions.json
           - ./rabbitmq.conf:/etc/rabbitmq/rabbitmq.conf
         networks:
           - rabbitmq-network
   ```

   Lastly notice the volumes we have used to predefine the `task_queue` and an administrative user with a username and password, `rabbitmq`, in the definitions file. The definitions file location is specified in the `rabbitmq.conf`, which is used to configure rabbitmq at buildtime. Because we defined `task_queue`, we no longer have to declare it in `send.py` and `receive.py`. 

   

2. **rabbitmq-consumer** built from the `consumer/Dockerfile`

   ```yaml
   rabbitmq-consumer:
   build: consumer
   container_name: rabbitmq-consumer
   depends_on:
       - rabbitmq-server
   networks:
       - rabbitmq-network
   tty: true
   ```

   The `tty: true` option keeps the container running, even after the entrypoint process is finished.

   The `consumer/Dockerfile` is not very complicated, but it adds the rabbitmq python library to our environment so our script will run properly. It also copies `receive.py` from the `consumer/` directory to the container.

   

3. **rabbitmq-producer** build from the `producer/Dockerfile`

   Equivalent to consumer, above.

### rabbitmq-network

We explicitely add a network, because according to Docker documenation it is good practice to delare one that isn't the default, even if you only include the default options. You can see that we added each service to this network, which means they can all refer to each other by their internal hostnames, which by default are the same name as the service.



## Running the full application

```bash
# Creates all three containers in the background
docker-compose up -d

# Enter an interactive shell from the consumer container
docker exec -it rabbitmq-consumer "/bin/bash"
# Start the receive script
python receive.py
# [*] Waiting for messages. To exit press CTRL+C
```

Open up another tab and start an interactive shell in the producer container

```bash
docker exec -it rabbitmq-producer "/bin/bash"
# Send a "hello world" over the docker network!
# Note that in send.py and receive.py, the hostname of the requested connection is 'rabbitmq-server' because the hostname of each container defaults to the name of the service (as defined in the docker-compose file)

python send.py
```



You should see a ` [x] Received 'Hello world!`. Congrats on your first multi-container docker build.