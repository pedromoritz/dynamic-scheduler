#!/bin/bash

# defining scheduler
CUSTOM_SCHEDULER="schedulerName: dynamic-scheduler"

# removing all workloads
kubectl delete pods --all -n default --grace-period 0 --force

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

# waiting for ready containers
sleep 30

# starting testset
k6 run -q --out csv=testcase-1_results.csv k6_script-testcase-1.js > /dev/null 2>&1

# starting dynamic scheduling
#./dynamic-scheduler-GreddyLB.py

