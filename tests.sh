#!/bin/bash

clean()
{
  kubectl delete namespace lab
  sleep 60
}

# 20 40 constant
clean
./run_kube-scheduler.sh pod_amount=20 target=40 rate_type=constant distribution=exponential metric=memory
clean
./run_kse.sh scheduler=GreedyLB pod_amount=20 target=40 rate_type=constant distribution=exponential metric=memory
clean
./run_kse.sh scheduler=RefineLB pod_amount=20 target=40 rate_type=constant distribution=exponential metric=memory

clean
./run_kube-scheduler.sh pod_amount=20 target=40 rate_type=constant distribution=exponential metric=cpu
clean
./run_kse.sh scheduler=GreedyLB pod_amount=20 target=40 rate_type=constant distribution=exponential metric=cpu
clean
./run_kse.sh scheduler=RefineLB pod_amount=20 target=40 rate_type=constant distribution=exponential metric=cpu

clean
./run_kube-scheduler.sh pod_amount=20 target=40 rate_type=constant distribution=normal metric=memory
clean
./run_kse.sh scheduler=GreedyLB pod_amount=20 target=40 rate_type=constant distribution=normal metric=memory
clean
./run_kse.sh scheduler=RefineLB pod_amount=20 target=40 rate_type=constant distribution=normal metric=memory

clean
./run_kube-scheduler.sh pod_amount=20 target=40 rate_type=constant distribution=normal metric=cpu
clean
./run_kse.sh scheduler=GreedyLB pod_amount=20 target=40 rate_type=constant distribution=normal metric=cpu
clean
./run_kse.sh scheduler=RefineLB pod_amount=20 target=40 rate_type=constant distribution=normal metric=cpu

# 20 40 ramp
clean
./run_kube-scheduler.sh pod_amount=20 target=40 rate_type=ramp distribution=exponential metric=memory
clean
./run_kse.sh scheduler=GreedyLB pod_amount=20 target=40 rate_type=ramp distribution=exponential metric=memory
clean
./run_kse.sh scheduler=RefineLB pod_amount=20 target=40 rate_type=ramp distribution=exponential metric=memory

clean
./run_kube-scheduler.sh pod_amount=20 target=40 rate_type=ramp distribution=exponential metric=cpu
clean
./run_kse.sh scheduler=GreedyLB pod_amount=20 target=40 rate_type=ramp distribution=exponential metric=cpu
clean
./run_kse.sh scheduler=RefineLB pod_amount=20 target=40 rate_type=ramp distribution=exponential metric=cpu

clean
./run_kube-scheduler.sh pod_amount=20 target=40 rate_type=ramp distribution=normal metric=memory
clean
./run_kse.sh scheduler=GreedyLB pod_amount=20 target=40 rate_type=ramp distribution=normal metric=memory
clean
./run_kse.sh scheduler=RefineLB pod_amount=20 target=40 rate_type=ramp distribution=normal metric=memory

clean
./run_kube-scheduler.sh pod_amount=20 target=40 rate_type=ramp distribution=normal metric=cpu
clean
./run_kse.sh scheduler=GreedyLB pod_amount=20 target=40 rate_type=ramp distribution=normal metric=cpu
clean
./run_kse.sh scheduler=RefineLB pod_amount=20 target=40 rate_type=ramp distribution=normal metric=cpu

clean

