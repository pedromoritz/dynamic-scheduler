#!/bin/bash

clean()
{
  kubectl delete namespace lab
  sleep 60
}

# constant exponential
clean
./run_kube-scheduler.sh pod_amount=$1 target=$2 rate_type=constant distribution=exponential metric=memory
clean
./run_kse.sh scheduler=GreedyLB pod_amount=$1 target=$2 rate_type=constant distribution=exponential metric=memory
clean
./run_kse.sh scheduler=RefineLB pod_amount=$1 target=$2 rate_type=constant distribution=exponential metric=memory

clean
./run_kube-scheduler.sh pod_amount=$1 target=$2 rate_type=constant distribution=exponential metric=cpu
clean
./run_kse.sh scheduler=GreedyLB pod_amount=$1 target=$2 rate_type=constant distribution=exponential metric=cpu
clean
./run_kse.sh scheduler=RefineLB pod_amount=$1 target=$2 rate_type=constant distribution=exponential metric=cpu

# constant normal
clean
./run_kube-scheduler.sh pod_amount=$1 target=$2 rate_type=constant distribution=normal metric=memory
clean
./run_kse.sh scheduler=GreedyLB pod_amount=$1 target=$2 rate_type=constant distribution=normal metric=memory
clean
./run_kse.sh scheduler=RefineLB pod_amount=$1 target=$2 rate_type=constant distribution=normal metric=memory

clean
./run_kube-scheduler.sh pod_amount=$1 target=$2 rate_type=constant distribution=normal metric=cpu
clean
./run_kse.sh scheduler=GreedyLB pod_amount=$1 target=$2 rate_type=constant distribution=normal metric=cpu
clean
./run_kse.sh scheduler=RefineLB pod_amount=$1 target=$2 rate_type=constant distribution=normal metric=cpu

# ramp exponential
clean
./run_kube-scheduler.sh pod_amount=$1 target=$2 rate_type=ramp distribution=exponential metric=memory
clean
./run_kse.sh scheduler=GreedyLB pod_amount=$1 target=$2 rate_type=ramp distribution=exponential metric=memory
clean
./run_kse.sh scheduler=RefineLB pod_amount=$1 target=$2 rate_type=ramp distribution=exponential metric=memory

clean
./run_kube-scheduler.sh pod_amount=$1 target=$2 rate_type=ramp distribution=exponential metric=cpu
clean
./run_kse.sh scheduler=GreedyLB pod_amount=$1 target=$2 rate_type=ramp distribution=exponential metric=cpu
clean
./run_kse.sh scheduler=RefineLB pod_amount=$1 target=$2 rate_type=ramp distribution=exponential metric=cpu

# ramp normal
clean
./run_kube-scheduler.sh pod_amount=$1 target=$2 rate_type=ramp distribution=normal metric=memory
clean
./run_kse.sh scheduler=GreedyLB pod_amount=$1 target=$2 rate_type=ramp distribution=normal metric=memory
clean
./run_kse.sh scheduler=RefineLB pod_amount=$1 target=$2 rate_type=ramp distribution=normal metric=memory

clean
./run_kube-scheduler.sh pod_amount=$1 target=$2 rate_type=ramp distribution=normal metric=cpu
clean
./run_kse.sh scheduler=GreedyLB pod_amount=$1 target=$2 rate_type=ramp distribution=normal metric=cpu
clean
./run_kse.sh scheduler=RefineLB pod_amount=$1 target=$2 rate_type=ramp distribution=normal metric=cpu

clean

