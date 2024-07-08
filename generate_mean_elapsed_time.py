#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from bs4 import BeautifulSoup
import csv

if sys.argv[1:]:
  workload_type = sys.argv[1]
  if workload_type == 'synthetic':
    pods = [20, 40]
  elif workload_type == 'realistic':
    pods = [10, 20]
  else:
    print('usage: generate_mean_elapsed_time.py synthetic|realistic')
    sys.exit()
else:
  print('usage: generate_mean_elapsed_time.py synthetic|realistic')
  sys.exit()

lang = 'pt' 
constantStr = 'constante' if lang == 'pt' else 'constant'
linearStr = 'linear' if lang == 'pt' else 'linear'
elapsedTimeStr = 'Duração da Requisição' if lang == 'pt' else 'Elapsed Time'

targets = [20, 40]
rates = ['constant', 'ramp']
distributions = ['exponential', 'normal']
metrics = ['memory', 'cpu']
algos = ['kube-scheduler', 'kse-GreedyLB', 'kse-RefineLB']
executions = ['results_1', 'results_2', 'results_3', 'results_4', 'results_5', 'results_6', 'results_7', 'results_8', 'results_9', 'results_10']

def save_grouped_graphics(distribution, metric):
  executions_data = defaultdict(dict)
  scenarios = []
  et_data = {'kube-scheduler': [], 'kse-GreedyLB': [], 'kse-RefineLB': []}
  std_data = {'kube-scheduler': [], 'kse-GreedyLB': [], 'kse-RefineLB': []}
  for rate in rates:
    for target in targets:
      for pod in pods:
        key = str(pod) + '_' + str(target) + '_' + rate + '_' + distribution + '_' + metric
        if rate == 'constant':
          scenarios.append(str(pod)+' pods\n'+str(target)+' req/s\n'+constantStr)
        elif rate == 'ramp': 
          scenarios.append(str(pod)+' pods,\n'+str(target)+' req/s\n'+linearStr)  
        for algo in algos:
          data_array = []
          for execution in executions:
            try:
              elapsed_time = get_requests_count(execution, algo+'_'+key)  
              data_array.append(float(elapsed_time))
            except Exception as error:
              data_array.append(100)
          et_data[algo].append(round(np.mean(data_array), 2))
          std_data[algo].append(round(np.std(data_array), 2))

  print(et_data)
  #x = np.arange(len(scenarios))
  #idth = 0.25
  #multiplier = 0
  #plt.figure().set_figwidth(12)
  #fig, ax = plt.subplots(figsize=(14,3.1))
  #try:
  #  for attribute, measurement in et_data.items():
  #    offset = width * multiplier
  #    std = std_data[attribute]
  #    rects = ax.bar(x + offset, measurement, width, yerr=std, capsize=5, label=attribute)
  #    multiplier += 1
  #  ax.set_ylim(0, 5000)
  #  ax.set_ylabel(elapsedTimeStr + '(ms)', fontsize=12)
  #  ax.set_xticks(x + width, scenarios, fontsize=12)
  #  ax.tick_params(axis='y', labelsize=12)
  #  ksl = mpatches.Patch(color='#1f77b4', label='Kube-Scheduler')
  #  ksegl = mpatches.Patch(color='#ff7f0e', label='KSE-GreedyLB')
  #  kserl = mpatches.Patch(color='#2ca02c', label='KSE-RefineLB')
  #  ax.grid(axis="y")
  #  ax.set_axisbelow(True)
  #  ax.legend(handles=[ksl, ksegl, kserl], loc='lower right', fontsize=12)
  #  plt.savefig('grouped_mean_elapsed_time_'+distribution+'_'+metric+'.svg', dpi=150, transparent=False, bbox_inches='tight', format='svg')
  #except Exception as error:
  #  print(error)
  #finally:
  #  plt.close()
  #  plt.cla()
  #  plt.clf()

def get_requests_count(execution, filename):
  try:
    with open(execution + '/summary_'+filename+'.html', 'r') as fp:
      soup = BeautifulSoup(fp, "html.parser")
      table = soup.find("div", class_="table-responsive")
      elements = table.find_all('td')[3].string.split()[0]
      return elements
  except Exception as error:
    return 0.0

save_grouped_graphics('normal', 'memory')
save_grouped_graphics('normal', 'cpu')
save_grouped_graphics('exponential', 'memory')
save_grouped_graphics('exponential', 'cpu')

