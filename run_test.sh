#!/bin/bash
reset

echo "NAMESPACE SETUP..."
kubectl delete namespaces lab1
kubectl create namespace lab1

echo "CREATING PODS..."
kubectl apply -f pods/pod-$1.yaml

sleep 20

echo "INCREASING MEMORY..."
#hey -n 1000 -c 1 -o csv http://192.168.59.121:31001/memory/increase > $1.csv
hey -n 1000 -c 1 http://192.168.59.121:31001/memory/increase

# TODO
# hey: exibir timestamp no csv 
# hey: tempo entre requisicoes via parametro
# hey: exibir erro no csv quando o alvo não responder
# balancer: criar estrategia para zero timeout no balanceamento
# balancer: distribuir os pods via outro scheduler

