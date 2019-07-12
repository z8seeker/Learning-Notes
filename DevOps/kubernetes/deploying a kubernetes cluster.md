# Deploying a Kubernetes Cluster

## Installing Kubernetes Locally Using minikube

Create a local VM, provision Kubernetes, and create alocal kubectl configuration that points to that cluster: 

```bash
minikube start
```

When you are done with your cluster, you can stop the VM with:

```bash
minikube stop
```

If you want to remove the cluster, you can run:

```bash
minikube delete
```

## The kubernetes Client

The official Kubernetes client is kubectl. kubectl can be used to manage most Kubernetes objects such as pods, ReplicaSets, and services. kubectl can also be used to explore and verify the overall health of the cluster.

checking cluster status:

```bash
kubectl version
```

This will display two different versions: the version of the local kubectl tool, as well as the version of the Kubernetes API server.

We can get a simple diagnostic for the cluster. This is a good way to verify that your cluster is generally healthy:

```bash
kubectl get componentstatuses
```

we can list out all of the nodes in our cluster:

```bash
kubectl get nodes
```

use the kubectl describe command to get more information about a specific node:

```bash
kubectl describe nodes NodeName
kubectl describe pods PodName
```

