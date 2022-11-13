#!/bin/bash

# defining scheduler
CUSTOM_SCHEDULER="schedulerName: dynamic-scheduler"

# removing all workloads
kubectl delete pods --all -n lab --grace-period 0 --force
kubectl delete namespaces lab
kubectl create namespace lab

# creating workloads
for i in 1 2 3 4 5 6; do	
	POD_NAME=pod-$i
	NODE_PORT=3100$i
	template=`cat "pod-deployment-template.yaml" | sed "s/{{POD_NAME}}/$POD_NAME/g"`
	template=`echo "$template" | sed "s/{{NODE_PORT}}/$NODE_PORT/g"`
	template=`echo "$template" | sed "s/{{CUSTOM_SCHEDULER}}/$CUSTOM_SCHEDULER/g"`
	echo "$template" | kubectl apply -f -
done

# scheduling workloads for initial state (round robin)
./round_robin_scheduler.py

# starting dynamic scheduling
#./dynamic-scheduler-GreddyLB.py

# starting testset
