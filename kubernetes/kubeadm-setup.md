```bash
# create new
sudo kubeadm init
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown 1000:1000 $HOME/.kube/config
export KUBECONFIG=$HOME/.kube/config

# tear down old
sudo kubeadm reset
rm $HOME/.kube/config
# or create token for old (valid for 24 hours)
kubeadm token create

# configure networking for single node
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

# Install Weave Net (pod network)
sudo sysctl net.bridge.bridge-nf-call-iptables=1
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
# verify
kubectl get pods --all-namespaces
# untaint nodes that have one
kubectl taint nodes --all node-role.kubernetes.io/master-

# run "kubeadm join" command given in kubeadm init



#install weave net
sudo curl -L git.io/weave -o /usr/local/bin/weave
sudo chmod a+x /usr/local/bin/weave
sudo weave status
kubectl get pods -n kube-system -l name=weave-net -o wide



kubectl create deployment idata-pipeline --image=<docker-image>
kubectl get deployents
```



```bash
# all objects require a json or (but typically) yaml description
# Deploy such an object:
kubectl apply -f <file>
# expected output: deployment.<something> created
```

```yaml
# required fields
# find apiversion with "kubectl api-versions"
apiVersion: apps/v1
kind: Deployment
metadata: 
	name: <unique-identifier>
  # UID:
  # namespace
# spec format is different for every kubernetes object and contains nested fields specific to that object
spec: 
  containers:
    - name: nginx
      image: nginx:1.7.9
      ports:
      - containerPort: 80

```

```yaml
# each pod is assigned a unique IP
# Every container in a Pod shares the network namespace, including the IP address and network ports
# localhost
# When containers in a Pod communicate with entities outside the Pod, they must coordinate how they use the shared network resources (such as ports)
# pod template: 
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo Hello Kubernetes! && sleep 3600']
```

```yaml
# service example:
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```





```bash
FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -oyaml'

apiVersion: v1
data:
  ClusterConfiguration: |
    apiServer:
      extraArgs:
        authorization-mode: Node,RBAC
      timeoutForControlPlane: 4m0s
    apiVersion: kubeadm.k8s.io/v1beta2
    certificatesDir: /etc/kubernetes/pki
    clusterName: kubernetes
    controllerManager: {}
    dns:
      type: CoreDNS
    etcd:
      local:
        dataDir: /var/lib/etcd
    imageRepository: k8s.gcr.io
    kind: ClusterConfiguration
    kubernetesVersion: v1.16.6
    networking:
      dnsDomain: cluster.local
      serviceSubnet: 10.96.0.0/12
    scheduler: {}
  ClusterStatus: |
    apiEndpoints:
      ip-172-31-16-63:
        advertiseAddress: 172.31.16.63
        bindPort: 6443
    apiVersion: kubeadm.k8s.io/v1beta2
    kind: ClusterStatus
kind: ConfigMap
metadata:
  creationTimestamp: "2020-01-23T20:37:58Z"
  name: kubeadm-config
  namespace: kube-system
  resourceVersion: "151"
  selfLink: /api/v1/namespaces/kube-system/configmaps/kubeadm-config
  uid: dc90aed0-c6a1-41a5-992a-5dfa338069d9
```

```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown 1000:1000 $HOME/.kube/config
export KUBECONFIG=$HOME/.kube/config
kubectl taint nodes --all node-role.kubernetes.io/master-

sudo docker run -i --entrypoint="/bin/bash" --name pipeline-container  -p 5671:5671 rabbitmq-pipeline 
```

kubectl create deployment idata-pipeline --image=<docker-image>
kubectl get deplyents

```bash

```

Docker Pre-pulled Images on Kubernetes

- all pods can use any images cached on a node
- requires root access to all nodes to setup
- `imagePullPolicy` property of the container is set to `IfNotPresent` or `Never`, then a local image is used (preferentially or exclusively, respectively).

```bash
# Install docker on base machine w/ kubernetes

# Install Docker CE
## Set up the repository:
### Install packages to allow apt to use a repository over HTTPS
sudo apt-get update && sudo apt-get install \
  apt-transport-https ca-certificates curl software-properties-common

### Add Docker’s official GPG key
sudo sh
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
exit

### Add Docker apt repository.
sudo add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"

## Install Docker CE.
sudo apt-get update && sudo apt-get install \
  containerd.io=1.2.10-3 \
  docker-ce=5:19.03.4~3-0~ubuntu-$(lsb_release -cs) \
  docker-ce-cli=5:19.03.4~3-0~ubuntu-$(lsb_release -cs)

# Setup daemon.
cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF

sudo mkdir -p /etc/systemd/system/docker.service.d

# Restart docker.
systemctl daemon-reload
systemctl restart docker

# install kubeadm

sudo apt-get install -y iptables arptables ebtables
# ensure legacy binaries are installed
sudo apt-get install -y iptables arptables ebtables

# switch to legacy versions
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
sudo update-alternatives --set arptables /usr/sbin/arptables-legacy
sudo update-alternatives --set ebtables /usr/sbin/ebtables-legacy

# install kubeadm, kublet, and kubectl
sudo apt-get update && sudo apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

```



A service is like a virtual server ndoe

```
spec:
	type: ClusterIP/NodePort
	ports:
		- targetPort (on pod): 80
			port ( on service)
			nodePort: 300008
	 - selector: # links the service to the pod
	 		app: myapp # this stuff matches the labels: in the pod definition
	 		type: messanger
	 		
```



