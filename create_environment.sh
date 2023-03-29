#!/bin/bash
minikube stop -p ppgcc
minikube delete -p ppgcc
minikube start --nodes 4 -p ppgcc --cpus 2 --memory 2048 --disk-size 2G --driver=docker --kubernetes-version v1.26.1
kubectl apply -f metrics-server.yaml
