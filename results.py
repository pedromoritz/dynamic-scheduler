#!/usr/bin/env python3

import os
from pathlib import Path
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

sd = defaultdict(dict)

pods = [20, 40]
targets = [20, 40]
rates = ['constant', 'ramp']
distributions = ['exponential', 'normal']
metrics = ['memory', 'cpu']
algos = ['kube-scheduler', 'kse-GreedyLB', 'kse-RefineLB']

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

def get_datasets():
  for path in sorted(Path("results/").glob("metrics_*.csv"), reverse=True):
    FILE_NAME, FILE_EXTENSION = os.path.splitext(path)
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

get_datasets()

def get_migrations_count(filename):
  try:
    with open(r"results/migrations_"+filename+'.csv', 'r') as fp:
      return len(fp.readlines())
  except Exception as error:
    return 0

def get_requests_count(filename):
  try:
    with open(r"results/summary_"+filename+'.html', 'r') as fp:
      soup = BeautifulSoup(fp, "html.parser")
      elements = soup.find_all("div", class_="bignum")
      return {
        'total': elements[0].string,
        'failed': elements[1].string
      }
  except Exception as error:
    return {
      'total': 0,
      'failed': 0
    }

def get_availability(total, failed):
  return str(round((total - failed) / ((total - failed) + failed) * 100, 2))

for pod in pods:
  for target in targets:
    for rate in rates:
      for distribution in distributions:
        for metric in metrics:
          key = str(pod) + '_' + str(target) + '_' + rate + '_' + distribution + '_' + metric
          for algo in algos:
            try:
              count = get_migrations_count(algo+'_'+key)
              requests = get_requests_count(algo+'_'+key)
              total = str(requests['total'])
              failed = str(requests['failed'])
              scenario = '\multirow{3}{*}{1}' if algo == 'kube-scheduler' else ''
              print(scenario+' & '+algo+' & '+sd[key][algo]['mae']+' & '+str(count)+' & '+total+' & '+failed+' & '+get_availability(int(total), int(failed))+'\%\\\\')
            except Exception as error:
              print(error)
          # saving graphic
          save_graphic(float(sd[key]['kube-scheduler']['mae']), float(sd[key]['kse-GreedyLB']['mae']), float(sd[key]['kse-RefineLB']['mae']), key+'.png')

