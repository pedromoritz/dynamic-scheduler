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
  IP=`minikube ip -p ppgcc`

  # starting testset
  k6 run -q --out csv="results/results_${ST}_${PA}_${TA}_${RT}_${DI}_${ME}.gz" -e IP=$IP -e ST=$ST -e PA=$PA -e TA=$TA -e RT=$RT -e DI=$DI -e ME=$ME k6_script-${RT}.js >/dev/null 2>&1 &

  # metrics monitoring
  ./kse-GreedyLB.py $ST $PA $TA $RT $DI $ME
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
  echo "usage: ./run_kse-GreedyLB.sh pod_amount=<POD_AMOUNT> target=<TARGET> rate_type=<RATE_TYPE> distribution=<DISTRIBUTION> metric=<METRIC>"
else
  test kse-GreedyLB $pod_amount $target $rate_type $distribution $metric
fi
