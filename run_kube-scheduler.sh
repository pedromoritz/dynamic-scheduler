#!/bin/bash

test()
{
  ST=$1 # scheduler type
  PA=$2 # pod amount
  VU=$3 # target virtual users

  # purging old files
  rm results/*_${ST}_${PA}_${VU}.*

  # defining scheduler
  SCHEDULER=""

  # removing all workloads
  kubectl delete namespace lab
  kubectl create namespace lab

  NODES=("ppgcc-m02" "ppgcc-m03" "ppgcc-m04" "ppgcc-m05")

  DISTRIBUTION_ARRAY=()
  for i in $(seq $(expr $PA / ${#NODES[@]})); do
    DISTRIBUTION_ARRAY+=($(shuf -e "${NODES[@]}"))
  done

  # creating workloads
  for i in $(seq $PA); do	
    POD_NAME=pod-$i
    NODE_PORT=31$(printf %03d $i)
    template=`cat "pod_deployment_template.yaml" | sed "s/{{POD_NAME}}/$POD_NAME/g"`
    template=`echo "$template" | sed "s/{{NODE_PORT}}/$NODE_PORT/g"`
    template=`echo "$template" | sed "s/{{SCHEDULER}}/$SCHEDULER/g"`
    template=`echo "$template" | sed "s/{{NODE_NAME}}/nodeName: ${DISTRIBUTION_ARRAY[i]}/g"`
    echo "$template" | kubectl apply -f -
  done

  # waiting for ready containers
  sleep 60

  # retrieving service IP
  SVCIP=`minikube ip -p ppgcc`

  # starting testset
  k6 run -q --out csv="results/results_${ST}_${PA}_${VU}.gz" -e SVC_IP=$SVCIP -e SCHEDULER_TYPE=$ST -e POD_AMOUNT=$PA -e VIRTUAL_USERS=$VU k6_script-constant_rate.js >/dev/null 2>&1 &

  # metrics monitoring
  ./metrics_monitoring.py $ST $PA $VU
}

test kube-scheduler $1 $2
