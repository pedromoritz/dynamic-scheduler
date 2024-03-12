#!/bin/bash

pods_array=(20 40)
targets_array=(20 40)
rates_array=('constant' 'ramp')
distributions_array=('exponential' 'normal')
metrics_array=('memory' 'cpu')
WL=real

for PA in ${pods_array[@]}; do
  for TA in ${targets_array[@]}; do
    for RT in ${rates_array[@]}; do
      for DI in ${distributions_array[@]}; do
        for ME in ${metrics_array[@]}; do

          FILE=results/metrics_kube-scheduler_${PA}_${TA}_${RT}_${DI}_${ME}.csv
          if [ -f "$FILE" ]; then
            echo "$FILE exists."
          else 
            echo "$FILE does not exist."
            ./run_kube-scheduler_experiment.sh pod_amount=$PA target=$TA rate_type=$RT distribution=$DI metric=$ME workload=$WL
          fi

          FILE=results/metrics_kse-GreedyLB_${PA}_${TA}_${RT}_${DI}_${ME}.csv
          if [ -f "$FILE" ]; then
            echo "$FILE exists."
          else
            echo "$FILE does not exist."
            ./run_kse_experiment.sh scheduler=GreedyLB pod_amount=$PA target=$TA rate_type=$RT distribution=$DI metric=$ME workload=$WL
          fi

          FILE=results/metrics_kse-RefineLB_${PA}_${TA}_${RT}_${DI}_${ME}.csv
          if [ -f "$FILE" ]; then
            echo "$FILE exists."
          else
            echo "$FILE does not exist."
            ./run_kse_experiment.sh scheduler=RefineLB pod_amount=$PA target=$TA rate_type=$RT distribution=$DI metric=$ME workload=$WL
          fi

        done
      done
    done
  done
done

