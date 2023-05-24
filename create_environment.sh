#!/bin/bash
minikube stop -p ppgcc # stop cluster ppgcc
minikube delete -p ppgcc # remove cluster ppgcc
sleep 30
minikube start --nodes 1 -p ppgcc --cpus 2 --memory 2048 --disk-size 5G --vm --kubernetes-version v1.26.3 # add master node
minikube addons enable metrics-server -p ppgcc # add metrics-server to master node
sleep 60
minikube node add -p ppgcc # add 1st worker node
sleep 60
minikube node add -p ppgcc # add 2nd worker node
sleep 60
minikube node add -p ppgcc # add 3rd worker node
sleep 60
minikube node add -p ppgcc # add 4th worker node
