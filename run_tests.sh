#!/bin/bash

test()
{
  # defining scheduler
  if [ "$1" = "dynamic_scheduler_GreedyLB" ]; then
    CUSTOM_SCHEDULER="schedulerName: dynamic_scheduler"
  else
    CUSTOM_SCHEDULER=""
  fi

  # removing all workloads
  kubectl delete pods --all -n lab --grace-period 0 --force
  sleep 30  
  kubectl delete namespace lab
  kubectl create namespace lab

  # creating workloads
  for i in $(seq $2); do	
    POD_NAME=pod-$i
    NODE_PORT=31$(printf %03d $i)
    template=`cat "pod_deployment_template.yaml" | sed "s/{{POD_NAME}}/$POD_NAME/g"`
    template=`echo "$template" | sed "s/{{NODE_PORT}}/$NODE_PORT/g"`
    template=`echo "$template" | sed "s/{{CUSTOM_SCHEDULER}}/$CUSTOM_SCHEDULER/g"`
    echo "$template" | kubectl apply -f -
  done

  # scheduling workloads for initial state (round robin)
  if [ "$1" = "dynamic_scheduler_GreedyLB" ]; then
    ./round_robin_scheduler.py
  fi

  # waiting for ready containers
  sleep 30

  # starting testset
  k6 run -q --out csv=results_$1_$2.csv -e SCHEDULER_TYPE=$1 -e POD_AMOUNT=$2 k6_script.js >/dev/null 2>&1 &

  # scheduling workloads for initial state (round robin)
  if [ "$1" = "dynamic_scheduler_GreedyLB" ]; then
    ./dynamic_scheduler_GreedyLB.py
  else
    ./metrics_monitoring.py
  fi
}

test default_scheduler 6
sleep 600
test dynamic_scheduler_GreedyLB 6
