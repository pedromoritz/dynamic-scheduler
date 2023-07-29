#!/bin/bash

test()
{
  ST=$1 # scheduler type
  PA=$2 # pod amount
  TA=$3 # target
  RT=$4 # rate type
  DI=$5 # distribution
  ME=$6 # metric

  # purging old files
  rm results/*_${ST}_${PA}_${TA}_${RT}_${DI}_${ME}.*
  touch results/metrics_${ST}_${PA}_${TA}_${RT}_${DI}_${ME}.csv

  # defining scheduler
  SCHEDULER=""

  # removing all workloads
  kubectl delete namespace lab
  kubectl create namespace lab

  NODES=("ppgcc-m02" "ppgcc-m03" "ppgcc-m04" "ppgcc-m05")
  SHUFFLE_ARRAY=(0 2 1 3 1 1 1 0 2 1 0 0 0 3 3 2 2 3 2 3 0 2 1 3 1 1 1 0 2 1 0 0 0 3 3 2 2 3 2 3)

  # creating workloads
  for i in $(seq $PA); do	
    POD_NAME=pod-$(printf %02d $i)
    NODE_PORT=31$(printf %03d $i)
    template=`cat "pod_deployment_template.yaml" | sed "s/{{POD_NAME}}/$POD_NAME/g"`
    template=`echo "$template" | sed "s/{{NODE_PORT}}/$NODE_PORT/g"`
    template=`echo "$template" | sed "s/{{SCHEDULER}}/$SCHEDULER/g"`
    template=`echo "$template" | sed "s/{{NODE_NAME}}/nodeName: ${NODES[SHUFFLE_ARRAY[i-1]]}/g"`
    template=`echo "$template" | sed "s/{{METRIC}}/$ME/g"`
    echo "$template" | kubectl apply -f -
  done

  # waiting for ready containers
  sleep 60

  # retrieving service IP
  IP=`minikube ip -p ppgcc`

  # starting testset
  k6 run -q --out csv="results/results_${ST}_${PA}_${TA}_${RT}_${DI}_${ME}.gz" -e IP=$IP -e ST=$ST -e PA=$PA -e TA=$TA -e RT=$RT -e DI=$DI -e ME=$ME k6_script-${RT}.js >/dev/null 2>&1 &

  # avoiding 1st minute
  sleep 60

  # metrics monitoring
  ./metrics_monitoring.py $ST $PA $TA $RT $DI $ME

  # removing all workloads
  kubectl delete namespace lab
}

for ARGUMENT in "$@"
do
  KEY=$(echo $ARGUMENT | cut -f1 -d=)
  KEY_LENGTH=${#KEY}
  VALUE="${ARGUMENT:$KEY_LENGTH+1}"
  export "$KEY"="$VALUE"
done

if [ -z $pod_amount ] || [ -z $target ] || ([ "$rate_type" != "ramp" ] && [ "$rate_type" != "constant" ]) || ([ "$distribution" != "exponential" ] && [ "$distribution" != "normal" ]) || ([ "$metric" != "memory" ] && [ "$metric" != "cpu" ])
then
  echo "usage: ./run_kube-scheduler.sh pod_amount=<POD_AMOUNT> target=<TARGET> rate_type=<RATE_TYPE> distribution=<DISTRIBUTION> metric=<METRIC>"
else
  test kube-scheduler $pod_amount $target $rate_type $distribution $metric
fi
