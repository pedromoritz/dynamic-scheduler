## Dynamic Scheduler

The dynamic scheduler targets an application class of pods with the following characteristics:

- no volumes attached
- stateless
- variable workloads
- long-lived containers

This repository is organized as follows:

#### customapp
This folders stores the assets responsible for generating the customapp application, which is responsible for play the customer container role in the Kubernetes environment.

#### experiments
In this folder we have the Dynamic Scheduler core, the testing scenarios and all the artifacts required to run the experiments related to this work.

#### pods
Here we have templates to create the pods into the Kubernetes cluster.

#### results
All the experiments results such as logs, diagrams and graphs are stored in this folder.


## Cluster setup

#### Create Kubernetes cluster
minikube start --nodes 4 -p ppgcc --cpus 2 --memory 4096 --disk-size 20G --vm --kubernetes-version v1.25.3

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

./results_X.py > results/results.csv; ./graphics_generator.py; git add results/*.txt; git add results/*.csv; git add results/*.html; git add results/*.svg; git commit -m "update"; git push

#### Access tesla machine ####
ssh pedrocarvalho@lapesd-tesla.inf.ufsc.br

find . -type f -name "*.svg" -exec bash -c 'rsvg-convert -f pdf -o $0.pdf $0' {} \;
