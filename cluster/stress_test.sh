#!/bin/bash
reset

echo "NAMESPACE SETUP..."
kubectl delete namespaces lab1
kubectl create namespace lab1

echo "CREATING PODS..."
# quantidade de pods via parametro
kubectl apply -f ../pods/stress-pod-ppgcc-1.yaml
kubectl apply -f ../pods/stress-pod-ppgcc-2.yaml
kubectl apply -f ../pods/stress-pod-ppgcc-3.yaml

kubectl get pods --namespace lab1 -o wide
kubectl top nodes

#hey -n 1000 -c 1 -o csv http://192.168.59.117:31002/ping > $1.csv

# modificações no hey:
# exibir timestamp no csv 
# tempo entre requisicoes via parametro
# exibir erro no csv quando o alvo não responder

# criar estrategia para zero timeout no balanceamento
# distribuir os pods via outro scheduler



