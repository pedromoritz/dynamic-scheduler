#!/usr/bin/env python3

import os
from pathlib import Path
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

def save_grouped_graphics(distribution, metric):
  scenarios = []
  mae_data = {'kube-scheduler': [], 'kse-GreedyLB': [], 'kse-RefineLB': []}
  for rate in rates:
    for target in targets:
      for pod in pods:
         key = str(pod) + '_' + str(target) + '_' + rate + '_' + distribution + '_' + metric
         if rate == 'constant':
           scenarios.append(str(pod)+' pods\n'+str(target)+' req/s\n'+'constante')
         elif rate == 'ramp': 
           scenarios.append(str(pod)+' pods,\n'+str(target)+' req/s\n'+'rampa')  
         for algo in algos:
           try:
             mae_data[algo].append(float(sd[key][algo]['mae']))
           except Exception as error:
             print(error)

  x = np.arange(len(scenarios))
  width = 0.25
  multiplier = 0
  plt.figure().set_figwidth(12)
  fig, ax = plt.subplots(figsize=(14,4))
  try:
    for attribute, measurement in mae_data.items():
      offset = width * multiplier
      rects = ax.bar(x + offset, measurement, width, label=attribute)
      ax.bar_label(rects, padding=2, rotation=90, fontsize=9)
      multiplier += 1
    if metric == 'memory':
      ax.set_ylim(0, 300)
      ax.set_ylabel('memory (MB)', fontsize=12)
    elif metric == 'cpu':
      ax.set_ylim(0, 800)
      ax.set_ylabel('CPU (millicpu)', fontsize=12)
    ax.set_xticks(x + width, scenarios, fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ksl = mpatches.Patch(color='#1f77b4', label='kube-scheduler')
    ksegl = mpatches.Patch(color='#ff7f0e', label='KSE-GreedyLB')
    kserl = mpatches.Patch(color='#2ca02c', label='KSE-RefineLB')
    ax.legend(handles=[ksl, ksegl, kserl], loc='upper right', fontsize=12)
    plt.savefig('results/grouped_'+distribution+'_'+metric+'.svg', dpi=150, transparent=False, bbox_inches='tight', format='svg')
  except Exception as error:
    print(error)
  finally:
    plt.close()
    plt.cla()
    plt.clf()

def save_graphic(value1, value2, value3, filename):
  if 'memory' in filename:
    plt.ylim(0, 300)
    plt.ylabel('memory (MB)')
  elif 'cpu' in filename:
    plt.ylim(0, 800)
    plt.ylabel('CPU (millicpu)')
  x = ['kube-scheduler', 'KSE+GreedyLB', 'KSE+RefineLB']
  y = [value1, value2, value3]
  plt.bar(x, y)
  addlabels(x, y)
  plt.savefig('results/mae_'+filename, dpi=150, transparent=False, bbox_inches='tight', format='svg')
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
      key = FILE_NAME[FILE_NAME.find('_', FILE_NAME.find('_') + 1)+1:]
      algo = FILE_NAME.split('_')[1]
      sd[key][algo] = {
        'mae': '0.0'
      }

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

get_datasets()

for pod in pods:
  for target in targets:
    for rate in rates:
      for distribution in distributions:
        for metric in metrics:
          key = str(pod) + '_' + str(target) + '_' + rate + '_' + distribution + '_' + metric
          for algo in algos:
            try:
              migrations = get_migrations_count(algo+'_'+key)
              requests = get_requests_count(algo+'_'+key)
              total = str(requests['total'])
              failed = str(requests['failed'])
              print(sd[key][algo]['mae']+','+str(migrations)+','+total+','+failed)
            except Exception as error:
              total = 0
              failed = 0
              print('0, 0, 0')
              #print(error)
          # saving graphic
          try:
            save_graphic(float(sd[key]['kube-scheduler']['mae']), float(sd[key]['kse-GreedyLB']['mae']), float(sd[key]['kse-RefineLB']['mae']), key+'.svg')
          except Exception as error:
            save_graphic(0.0, 0.0, 0.0, key+'.svg')
            #print(error)

save_grouped_graphics('normal', 'memory')
save_grouped_graphics('normal', 'cpu')
save_grouped_graphics('exponential', 'memory')
save_grouped_graphics('exponential', 'cpu')
