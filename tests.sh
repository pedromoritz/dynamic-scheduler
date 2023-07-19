#!/bin/bash

pods_array=(20 40)
targets_array=(20 40)
rates_array=('constant' 'ramp')
distributions_array=('exponential' 'normal')
metrics_array=('memory' 'cpu')
algos_array=('kube-scheduler' 'kse-GreedyLB' 'kse-RefineLB')

for i in ${pods_array[@]}; do
  for j in ${targets_array[@]}; do
    for k in ${rates_array[@]}; do
      for l in ${distributions_array[@]}; do
        for m in ${metrics_array[@]}; do
          echo $i $j $k $l $m        
          ./run_kube-scheduler.sh pod_amount=$i target=$j rate_type=$k distribution=$l metric=$m
          ./run_kse.sh scheduler=GreedyLB pod_amount=$i target=$j rate_type=$k distribution=$l metric=$m
          ./run_kse.sh scheduler=RefineLB pod_amount=$i target=$j rate_type=$k distribution=$l metric=$m
        done
      done
    done
  done
done

