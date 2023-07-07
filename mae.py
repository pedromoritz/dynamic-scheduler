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
    plt.ylim(0, 500)
    plt.ylabel('memory (MB)')
  elif 'cpu' in filename:
    plt.ylim(0, 1000)
    plt.ylabel('CPU (millicpu)')
  x = ['kube-scheduler', 'KSE+GreedyLB', 'KSE+RefineLB']
  y = [value1, value2, value3]
  plt.bar(x, y)
  addlabels(x, y)
  plt.savefig('results/mae_'+filename, dpi=150, transparent=False, bbox_inches='tight')
  plt.close()
  plt.cla()
  plt.clf()

def f(number):
  return str(round(number, 2))

def get_mae(dataset):
  data_list = []
  for i in range(len(dataset[0])):
    pontual_metrics = []
    pontual_metrics.append(dataset[0][i])
    pontual_metrics.append(dataset[1][i])
    pontual_metrics.append(dataset[2][i])
    pontual_metrics.append(dataset[3][i])
    sorted_pontual_metrics = sorted(pontual_metrics)
    max_value = sorted_pontual_metrics[-1]
    min_value = sorted_pontual_metrics[0]
    data_list.append(max_value - min_value)
  return {
    'mae': f(np.average(data_list))
  }

for path in sorted(Path("results/").glob("metrics_*.csv"), reverse=True):
  FILE_NAME, FILE_EXTENSION = os.path.splitext(path)
  print(path)
  try:
    timestamp, n1_pod_amount, n1_memory, n1_cpu, n2_pod_amount, n2_memory, n2_cpu, n3_pod_amount, n3_memory, n3_cpu, n4_pod_amount, n4_memory, n4_cpu = np.loadtxt(FILE_NAME + '.csv', unpack=True, delimiter=',', skiprows=1)
    if 'memory' in FILE_NAME:
      # calculating mean absolute error
      dataset = []
      dataset.append(list(map(lambda n: n/1024, n1_memory)))
      dataset.append(list(map(lambda n: n/1024, n2_memory)))
      dataset.append(list(map(lambda n: n/1024, n3_memory)))
      dataset.append(list(map(lambda n: n/1024, n4_memory)))
      data = get_mae(dataset)
      key = FILE_NAME[FILE_NAME.find('_', FILE_NAME.find('_') + 1)+1:]
      algo = FILE_NAME.split('_')[1]
      sd[key][algo] = data
    elif 'cpu' in FILE_NAME:
      # calculating mean absolute error
      dataset = []
      dataset.append(list(map(lambda n: n/1000000, n1_cpu)))
      dataset.append(list(map(lambda n: n/1000000, n2_cpu)))
      dataset.append(list(map(lambda n: n/1000000, n3_cpu)))
      dataset.append(list(map(lambda n: n/1000000, n4_cpu)))
      data = get_mae(dataset)
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
      'mae': '0.0'
    }

for key in sd:
  try:
    algo = 'kube-scheduler'
    print(algo+','+key+','+sd[key][algo]['mae'])
    algo = 'kse-GreedyLB'
    print(algo+','+key+','+sd[key][algo]['mae'])
    algo = 'kse-RefineLB'
    print(algo+','+key+','+sd[key][algo]['mae'])
    save_graphic(float(sd[key]['kube-scheduler']['mae']), float(sd[key]['kse-GreedyLB']['mae']), float(sd[key]['kse-RefineLB']['mae']), key+'.png')
  except Exception as error:
    print(error)

