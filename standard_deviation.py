#!/usr/bin/env python3

import os
from pathlib import Path
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

sd = defaultdict(dict)

def addlabels(x,y):
  for i in range(len(x)):
    plt.text(i, y[i]+5, y[i], ha = 'center')

def save_graphic(value1, value2, value3, filename):
  if 'memory' in filename:
    plt.ylim(0, 200)
    plt.ylabel('memory (MB)')
  elif 'cpu' in filename:
    plt.ylim(0, 500)
    plt.ylabel('CPU (millicpu)')
  x = ['kube-scheduler', 'KSE+GreedyLB', 'KSE+RefineLB']
  y = [value1, value2, value3]
  plt.bar(x, y)
  addlabels(x, y)
  plt.savefig('results/standard-deviation_'+filename, dpi=150, transparent=False, bbox_inches='tight')
  plt.close()
  plt.cla()
  plt.clf()

def f(number):
  return str(round(number, 2))

def get_standard_deviation(dataset):
  data_list = []
  for data in dataset:
    data_list.append(round(np.average(data), 2))
  sorted_data_list = sorted(data_list)
  min_value = sorted_data_list[0]
  max_value = sorted_data_list[-1]
  mean = sum(data_list) / len(data_list)
  variance = sum([((x - mean) ** 2) for x in data_list]) / len(data_list)
  standard_deviation = variance ** 0.5
  return {
    'min': f(min_value),
    'max': f(max_value),
    'mean': f(mean),
    'sd': f(standard_deviation)
  }

for path in sorted(Path("results/").glob("metrics_*.csv"), reverse=True):
  FILE_NAME, FILE_EXTENSION = os.path.splitext(path)
  try:
    timestamp, n1_pod_amount, n1_memory, n1_cpu, n2_pod_amount, n2_memory, n2_cpu, n3_pod_amount, n3_memory, n3_cpu, n4_pod_amount, n4_memory, n4_cpu = np.loadtxt(FILE_NAME + '.csv', unpack=True, delimiter=',', skiprows=1)
    if 'memory' in FILE_NAME:
      # calculating memory standard deviation
      dataset = []
      dataset.append(list(map(lambda n: n/1024, n1_memory)))
      dataset.append(list(map(lambda n: n/1024, n2_memory)))
      dataset.append(list(map(lambda n: n/1024, n3_memory)))
      dataset.append(list(map(lambda n: n/1024, n4_memory)))
      data = get_standard_deviation(dataset)
      key = FILE_NAME[FILE_NAME.find('_', FILE_NAME.find('_') + 1)+1:]
      algo = FILE_NAME.split('_')[1]
      sd[key][algo] = data
    elif 'cpu' in FILE_NAME:
      # calculating cpu standard deviation
      dataset = []
      dataset.append(list(map(lambda n: n/1000000, n1_cpu)))
      dataset.append(list(map(lambda n: n/1000000, n2_cpu)))
      dataset.append(list(map(lambda n: n/1000000, n3_cpu)))
      dataset.append(list(map(lambda n: n/1000000, n4_cpu)))
      data = get_standard_deviation(dataset)
      key = FILE_NAME[FILE_NAME.find('_', FILE_NAME.find('_') + 1)+1:]
      algo = FILE_NAME.split('_')[1]
      sd[key][algo] = data
  except Exception as error:
    print(FILE_NAME + '.csv' + ' ---> ERROR')
    print(error)
    print('-')
    key = FILE_NAME[FILE_NAME.find('_', FILE_NAME.find('_') + 1)+1:]
    algo = FILE_NAME.split('_')[1]
    sd[key][algo] = {
      'min': '0.0',
      'max': '0.0',
      'mean': '0.0',
      'sd': '0.0'
    }

for key in sd:
  try: 
    algo = 'kube-scheduler'
    print(algo+','+key+','+sd[key][algo]['min']+','+sd[key][algo]['max']+','+sd[key][algo]['mean']+','+sd[key][algo]['sd'])
    algo = 'kse-GreedyLB'
    print(algo+','+key+','+sd[key][algo]['min']+','+sd[key][algo]['max']+','+sd[key][algo]['mean']+','+sd[key][algo]['sd'])
    algo = 'kse-RefineLB'
    print(algo+','+key+','+sd[key][algo]['min']+','+sd[key][algo]['max']+','+sd[key][algo]['mean']+','+sd[key][algo]['sd'])
    save_graphic(float(sd[key]['kube-scheduler']['sd']), float(sd[key]['kse-GreedyLB']['sd']), float(sd[key]['kse-RefineLB']['sd']), key+'.png')
  except Exception as error:
    print(error)
