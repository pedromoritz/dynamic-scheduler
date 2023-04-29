#!/bin/bash

test()
{
  ST=$1 # scheduler type
  PA=$2 # pod amount
  VU=$3 # target virtual users

  # purging old files
  rm results/*_${ST}_${PA}_${VU}.*

  # defining scheduler
  SCHEDULER="schedulerName: kse"
  NODE_NAME=""

  # removing all workloads
  kubectl delete namespace lab
  kubectl create namespace lab

  # creating workloads
  for i in $(seq $PA); do	
    POD_NAME=pod-$i
    NODE_PORT=31$(printf %03d $i)
    template=`cat "pod_deployment_template.yaml" | sed "s/{{POD_NAME}}/$POD_NAME/g"`
    template=`echo "$template" | sed "s/{{NODE_PORT}}/$NODE_PORT/g"`
    template=`echo "$template" | sed "s/{{SCHEDULER}}/$SCHEDULER/g"`
    template=`echo "$template" | sed "s/{{NODE_NAME}}/$NODE_NAME/g"`
    echo "$template" | kubectl apply -f -
  done

  # shuffle scheduler
  ./shuffle_scheduler.py

  # waiting for ready containers
  sleep 60

  # retrieving service IP
  SVCIP=`minikube ip -p ppgcc`
  
  # starting testset
  k6 run -q --out csv="results/results_${ST}_${PA}_${VU}.gz" -e SVC_IP=$SVCIP -e SCHEDULER_TYPE=$ST -e POD_AMOUNT=$PA -e VIRTUAL_USERS=$VU k6_script-constant_rate.js >/dev/null 2>&1 &

  # metrics monitoring
  ./kse-RefineLB.py $ST $PA $VU
}

test kse-RefineLB $1 $2
