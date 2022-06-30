#!/bin/bash

options=("kube-scheduler" "dynamic-scheduler")

if [[ " ${options[@]} " =~ " $1 " ]]; then
    echo "NAMESPACE SETUP..."
	kubectl delete namespaces lab1
	kubectl create namespace lab1

	echo "CREATING PODS..."
	kubectl apply -f pods/pod-$1.yaml

	sleep 20

	echo "INCREASING MEMORY..."
	#hey -n 10000 -c 10 -q 10 -o csv http://192.168.59.121:31001/memory/increase > csv/$1.csv
	hey -n 10000 -c 1 http://192.168.59.121:31001/memory/increase
else
	echo "usage:"
	echo "./run_test.sh kube-scheduler or"
	echo "./run_test.sh dynamic-scheduler"
fi
