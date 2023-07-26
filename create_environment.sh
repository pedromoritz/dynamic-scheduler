#!/bin/bash
minikube stop -p ppgcc # stop cluster ppgcc
minikube delete -p ppgcc # remove cluster ppgcc
minikube start --nodes 1 -p ppgcc --cpus 2 --memory 2G --disk-size 5G --container-runtime containerd --vm --kubernetes-version v1.27.3 # add master node
minikube addons enable metrics-server -p ppgcc # add metrics-server to master node
sleep 120
minikube node add -p ppgcc # add 1st worker node
sleep 120
minikube node add -p ppgcc # add 2nd worker node
sleep 120
minikube node add -p ppgcc # add 3rd worker node
sleep 120
minikube node add -p ppgcc # add 4th worker node
