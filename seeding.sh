#!/bin/bash

CUSTOM_SCHEDULER="schedulerName: dynamic-scheduler"

kubectl delete namespaces lab
kubectl create namespace lab

for i in 1 2 3 4 5 6; do	
	POD_NAME=pod-$i
	NODE_PORT=3100$i
	template=`cat "pods/pod-deployment-template.yaml" | sed "s/{{POD_NAME}}/$POD_NAME/g"`
	template=`echo "$template" | sed "s/{{NODE_PORT}}/$NODE_PORT/g"`
	template=`echo "$template" | sed "s/{{CUSTOM_SCHEDULER}}/$CUSTOM_SCHEDULER/g"`
	echo "$template" | kubectl apply -f -
done

./seeding_scheduler.py
