#!/bin/bash
reset
echo "NAMESPACE SETUP..."
kubectl delete namespaces lab1
kubectl create namespace lab1
echo "CREATING STRESSING PODS..."
kubectl apply -f ../pods/stressing-pod-ppgcc-m02.yaml
kubectl apply -f ../pods/stressing-pod-ppgcc-m03.yaml
kubectl apply -f ../pods/stressing-pod-ppgcc-m04.yaml
sleep 10
kubectl get pods --namespace lab1 -o wide
kubectl top nodes
echo "CREATING TARGET POD..."
kubectl apply -f ../pods/target-pod-default-scheduler.yaml
sleep 10
kubectl get pods --namespace lab1 -o wide
kubectl top nodes
CURRENT_NODE=$(kubectl get pods --namespace lab1 -o wide |grep target-pod-default-scheduler | awk -F ' ' '{print $7}')
echo "target pod encontrado no node $CURRENT_NODE"
NODE_NUMBER=${CURRENT_NODE: -2}
ab -S -n 75000 -c 1 http://192.168.59.117:310$NODE_NUMBER/ping
sleep 10
kubectl top nodes
kubectl get pods --namespace lab1 -o wide