# RabbitMQ Configuration Files Volume

## Static Configuration in Docker

When we build RabbitMQ with Docker, we have to make the configuration files available at buildtime, which means we can't simply add our configuration files with `COPY` in our Dockerfile. Instead, we will use `docker-compose` to mount our configuration files as volumes so they are available during the image build.

### docker-compose.yml

```yaml
rabbitmq-producer:
  labels:
    NAME: "rabbitmq-producer"
    MAINTAINER: "brewer36@purdue.edu"
  image: rabbitmq:latest
  ports:
    - "15672:15672"
    - "5672:5672"
  volumes:
    - ./definitions.json:/etc/rabbitmq/definitions.json
    - ./rabbitmq.config:/etc/rabbitmq/rabbitmq.config
```



### Build, Run, and Cleanup

```bash
# Build and run
docker-compose up

# Access the running docker container via it's command line
docker exec -it run-in-docker-with-config-files_rabbitmq_1 "/bin/bash"


# stop
docker-compose stop

# remove
docker-compose down

# remove containers AND volumes
docker-compose --volumes
```



## Static Configuration in Kubernetes

Volumes in Kubernetes are guarenteed to have the same lifetimes as the pods that enclose them, and are available to all containers in the pod

## Create ConfigMap

```bash
kubectl create configmap rabbitmq-config --from-file=rabbitmq.config
```



