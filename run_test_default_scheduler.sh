#!/bin/bash

test()
{
  # defining scheduler
  SCHEDULER=""

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

  # waiting for ready containers
  sleep 30

  # starting testset
  k6 run -q --out csv=results_default_scheduler_$1.csv -e SCHEDULER_TYPE=default_scheduler -e POD_AMOUNT=$1 k6_script.js >/dev/null 2>&1 &

  # metrics monitoring
  ./metrics_monitoring.py $1
}

test $1
