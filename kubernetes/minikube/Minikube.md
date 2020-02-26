# Minikube



## Optional: Using local docker images in minikube

```bash
# Start minikube
minikube start

# Set docker env
eval $(minikube docker-env)

# Build image
docker build -t py-server .
```



## Hello Minikube

```bash
# Start minikube
minikube start

# A pod is a group of one or more containers that make up a microservice
# A deployment creates, monitors the health of, scales, and restarts terminated pods
kubectl create deployment py-server --image=brewer36/py-server

# A pod is only accessible by its internal IP within the cluster
# To make a container (pod?) accessible outside the Kubernetes virtual network, we expose the pod as a service
kubectl expose deployment py-server --type=LoadBalancer --port=8080

# What is a load balancer?
# A LoadBalancer takes incoming traffic and routes the traffic to available instances, which in the case of a Kubernetes cluster, are NodePorts and ClusterIP services
# ClusterIP services are exposed on a cluster-internal IP
# NodePorts services are exposed on each node's IP at a static port. NodePorts are routed through a ClusterIP service (which is created automatically)

# View the LoadBalance service we just created
kubectl get services

# On a cloud provider that supports a load balancer, we would be provisioned an external IP in order to access the service
# Since we are using minikube, we can make this service available thorugh the command...
minikube service py-server

# This will open up a browser tab to the service URL, but if we want to work from the terminal, we can save the URL to variable
PY_SERVER_URL=$(minikube service py-server --url)
# and then we can make a URL request from the command line with
curl $PY_SERVER_URL
```



## Scaling

```bash
# Horizontal Scaling with ReplicaSets
# ReplicaSets ensure that a specified number of pod replicas are running at any time

kubectl scale deployment py-server --replicas=3

# Confirm there are now 3 replica sets
kubectl get pods

# Now when we curl several times, we will see that the pod that recieves our request is selected by the LoadBalancer at random
curl $PY_SERVER_URL
curl $PY_SERVER_URL
curl $PY_SERVER_URL
curl $PY_SERVER_URL
# Pods and their addresses come and go, but the service always has the same address with which we can communicate

```



## Cleanup

```bash
kubectl delete service py-server
kubectl delete deployment py-server
minikube stop
minikube delete
```

