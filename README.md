## Dynamic Scheduler

The dynamic scheduler targets an application class of pods with the following characteristics:

- no volumes attached
- stateless
- variable workloads
- long-lived containers


This repository is organized as follows:

#### customapp
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet neque aliquet, finibus diam eu, sollicitudin sapien.

#### experiments
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet neque aliquet, finibus diam eu, sollicitudin sapien.

#### pods
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet neque aliquet, finibus diam eu, sollicitudin sapien.

#### results
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet neque aliquet, finibus diam eu, sollicitudin sapien.

## Cluster setup

#### Create Kubernetes cluster
#minikube start --nodes 4 -p ppgcc --cpus 2 --memory 2000 --vm --kubernetes-version=v1.24.3
minikube start --nodes 3 -p ppgcc --cpus 2 --memory 1900 --vm --kubernetes-version=v1.24.3

#### Enable Metrics API
minikube addons enable metrics-server -p ppgcc

#### Create "lab" namespace
kubectl create namespace lab


## Useful commands

#### Remove deployments from "lab" namespace
kubectl --namespace lab delete deployments `kubectl get deployments --namespace lab --no-headers -o custom-columns=":metadata.name"`

#### Remove pods from "lab" namespace
kubectl --namespace lab delete pod `kubectl get pods --namespace lab --no-headers -o custom-columns=":metadata.name"`

#### Purge "ppgcc" minikube profile
minikube delete -p ppgcc

#### List minikube services
minikube service list -p ppgcc

#### List pods info at "lab" namespace
kubectl get pods --namespace lab -o wide

#### Show pods resources at "lab" namespace
kubectl top node --namespace lab

#### Show nodes through Metrics API
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes

#### Generate class and packages diagram
sudo apt install pylint graphviz

pyreverse -p Dynamic-Scheduler -o png -d results experiments
