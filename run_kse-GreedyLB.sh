#!/bin/bash

test()
{
  # defining scheduler
  SCHEDULER="schedulerName: kse"

  # removing all workloads
  kubectl delete namespace lab
  kubectl create namespace lab

  # creating workloads
  for i in $(seq $1); do	
    POD_NAME=pod-$i
    NODE_PORT=31$(printf %03d $i)
    template=`cat "pod_deployment_template.yaml" | sed "s/{{POD_NAME}}/$POD_NAME/g"`
    template=`echo "$template" | sed "s/{{NODE_PORT}}/$NODE_PORT/g"`
    template=`echo "$template" | sed "s/{{SCHEDULER}}/$SCHEDULER/g"`
    echo "$template" | kubectl apply -f -
  done

  # round robin scheduler
  ./round_robin_scheduler.py

  # waiting for ready containers
  sleep 30

  # starting testset
  k6 run -q --out csv=results_kse-GreedyLB_$1_pods.csv -e SCHEDULER_TYPE=kse-GreedyLB -e POD_AMOUNT=$1 k6_script.js >/dev/null 2>&1 &

  # metrics monitoring
  ./kse-GreedyLB.py $1
}

test $1

