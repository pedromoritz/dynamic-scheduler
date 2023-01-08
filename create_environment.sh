#!/bin/bash
minikube stop -p ppgcc
minikube delete -p ppgcc
minikube start --nodes 2 -p ppgcc --cpus 2 --memory 2048 --disk-size 2G --vm --kubernetes-version v1.25.3
minikube addons enable metrics-server -p ppgcc

