#!/usr/bin/env python3

import os
from pathlib import Path
import numpy as np

def get_standard_deviation(label, dataset):
  print('-------------------------------------------')
  print(label)
  data_list = []
  for data in dataset:
    data_list.append(round(np.average(data), 2))
  sorted_data_list = sorted(data_list)
  min_value = sorted_data_list[0]
  max_value = sorted_data_list[-1]
  print(' min: ' + str(round(min_value, 2)))
  print(' max: ' + str(round(max_value, 2)))
  mean = sum(data_list) / len(data_list)
  print('mean: ' + str(round(mean, 2)))
  variance = sum([((x - mean) ** 2) for x in data_list]) / len(data_list)
  standard_deviation = round(variance ** 0.5, 2)
  print('  sd: ' + str(standard_deviation))

for path in Path("results/").glob("metrics_*.csv"):
  FILE_NAME, FILE_EXTENSION = os.path.splitext(path)
  timestamp, node1_pod_amount, node1_memory, node1_cpu, node2_pod_amount, node2_memory, node2_cpu, node3_pod_amount, node3_memory, node3_cpu, node4_pod_amount, node4_memory, node4_cpu = np.loadtxt(FILE_NAME + '.csv', unpack=True, delimiter=',', skiprows=1)

  if 'kube-scheduler' in FILE_NAME:
    # calculating memory standard deviation
    dataset = []
    dataset.append(list(map(lambda n: n/1024, node1_memory)))
    dataset.append(list(map(lambda n: n/1024, node2_memory)))
    dataset.append(list(map(lambda n: n/1024, node3_memory)))
    dataset.append(list(map(lambda n: n/1024, node4_memory)))
    get_standard_deviation(FILE_NAME + "_memory", dataset)
    # calculating cpu standard deviation
    dataset = []
    dataset.append(list(map(lambda n: n/1000000, node1_cpu)))
    dataset.append(list(map(lambda n: n/1000000, node2_cpu)))
    dataset.append(list(map(lambda n: n/1000000, node3_cpu)))
    dataset.append(list(map(lambda n: n/1000000, node4_cpu)))
    get_standard_deviation(FILE_NAME + "_cpu", dataset)
  elif 'kse' in FILE_NAME:
    if 'memory' in FILE_NAME:
      # calculating memory standard deviation
      dataset = []
      dataset.append(list(map(lambda n: n/1024, node1_memory)))
      dataset.append(list(map(lambda n: n/1024, node2_memory)))
      dataset.append(list(map(lambda n: n/1024, node3_memory)))
      dataset.append(list(map(lambda n: n/1024, node4_memory)))
      get_standard_deviation(FILE_NAME, dataset)
    elif 'cpu' in FILE_NAME:
      # calculating cpu standard deviation
      dataset = []
      dataset.append(list(map(lambda n: n/1000000, node1_cpu)))
      dataset.append(list(map(lambda n: n/1000000, node2_cpu)))
      dataset.append(list(map(lambda n: n/1000000, node3_cpu)))
      dataset.append(list(map(lambda n: n/1000000, node4_cpu)))
      get_standard_deviation(FILE_NAME, dataset)

