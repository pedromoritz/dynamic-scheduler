#!/bin/bash

options=("kube-scheduler" "dynamic-scheduler")

if [[ " ${options[@]} " =~ " $1 " ]]; then
    echo "NAMESPACE SETUP..."
	kubectl delete namespaces lab1
	kubectl create namespace lab1

	echo "CREATING PODS..."
	for i in 1 2 3 4 5; do	
		POD_NAME=pod-$1-$i
		NODE_PORT=3100$i
		CUSTOM_SCHEDULER=""

		if [[ "dynamic-scheduler" == "$1" ]]; then
			CUSTOM_SCHEDULER="schedulerName: dynamic-scheduler"
		fi

		template=`cat "pods/pod-deployment-template.yaml" | sed "s/{{POD_NAME}}/$POD_NAME/g"`
		template=`echo "$template" | sed "s/{{NODE_PORT}}/$NODE_PORT/g"`
		template=`echo "$template" | sed "s/{{CUSTOM_SCHEDULER}}/$CUSTOM_SCHEDULER/g"`
		echo "$template" | kubectl apply -f -
	done

	sleep 20

	echo "INCREASING MEMORY..."
	for i in 1 2 3 4 5; do
  		hey -n 10000 -c 1 http://192.168.59.121:3100$i/memory/increase &
	   #hey -n 10000 -c 10 -q 10 -o csv http://192.168.59.121:31001/memory/increase > csv/$1.csv
  	done
else
	echo "usage:"
	echo "./run_test.sh kube-scheduler or"
	echo "./run_test.sh dynamic-scheduler"
fi
