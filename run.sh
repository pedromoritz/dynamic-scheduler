#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: ./run.sh <SCHEDULER_TYPE: default-scheduler | dynamic-scheduler-GreedyLB> <POD_AMOUNT>"
  exit 1
fi

# defining scheduler
if [ "$1" = "dynamic-scheduler-GreedyLB" ]; then
  CUSTOM_SCHEDULER="schedulerName: dynamic-scheduler"
else
  CUSTOM_SCHEDULER=""
fi

# removing all workloads
kubectl delete pods --all -n lab --grace-period 0 --force
kubectl delete namespace lab
kubectl create namespace lab

# creating workloads
for i in $(seq $2); do	
  POD_NAME=pod-$i
  NODE_PORT=31$(printf %03d $i)
  template=`cat "pod-deployment-template.yaml" | sed "s/{{POD_NAME}}/$POD_NAME/g"`
  template=`echo "$template" | sed "s/{{NODE_PORT}}/$NODE_PORT/g"`
  template=`echo "$template" | sed "s/{{CUSTOM_SCHEDULER}}/$CUSTOM_SCHEDULER/g"`
  echo "$template" | kubectl apply -f -
done

# scheduling workloads for initial state (round robin)
if [ "$1" = "dynamic-scheduler-GreedyLB" ]; then
  ./round-robin-scheduler.py
fi

# waiting for ready containers
sleep 30

# starting testset
k6 run -q --out csv=temp_results.csv -e SCHEDULER_TYPE=$1 -e POD_AMOUNT=$2 k6_script.js &

# scheduling workloads for initial state (round robin)
if [ "$1" = "dynamic-scheduler-GreedyLB" ]; then
  ./dynamic-scheduler-GreedyLB.py
fi

