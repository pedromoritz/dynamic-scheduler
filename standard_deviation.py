#!/usr/bin/env python3

import os
from pathlib import Path
import numpy as np

def get_standard_deviation(dataset):
  data_list = []
  for data in dataset:
    data_list.append(round(np.average(data), 2))
  mean = sum(data_list) / len(data_list)
  variance = sum([((x - mean) ** 2) for x in data_list]) / len(data_list)
  return round(variance ** 0.5, 2)

for path in Path("results/").glob("metrics_*.csv"):
  FILE_NAME, FILE_EXTENSION = os.path.splitext(path)
  timestamp, node1_pod_amount, node1_memory, node1_cpu, node2_pod_amount, node2_memory, node2_cpu, node3_pod_amount, node3_memory, node3_cpu, node4_pod_amount, node4_memory, node4_cpu = np.loadtxt(FILE_NAME + '.csv', unpack=True, delimiter=',', skiprows=1)

  if 'memory' in FILE_NAME:
    # calculating memory standard deviation
    dataset = []
    dataset.append(node1_memory)
    dataset.append(node2_memory)
    dataset.append(node3_memory)
    dataset.append(node4_memory)
    print(FILE_NAME + ": " + str(get_standard_deviation(dataset)))

  elif 'cpu' in FILE_NAME:
    # calculating cpu standard deviation
    dataset = []
    dataset.append(node1_cpu)
    dataset.append(node2_cpu)
    dataset.append(node3_cpu)
    dataset.append(node4_cpu)
    print(FILE_NAME + ": " + str(get_standard_deviation(dataset)))

