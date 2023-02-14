#!/bin/bash
minikube stop -p ppgcc
minikube delete -p ppgcc
minikube start --nodes 4 -p ppgcc --cpus 2 --memory 4096 --disk-size 10G --vm --kubernetes-version v1.25.3
minikube addons enable metrics-server -p ppgcc

