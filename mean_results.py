#!/usr/bin/env python3

import os
from pathlib import Path
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from bs4 import BeautifulSoup
import csv

pods = [20, 40]
targets = [20, 40]
rates = ['constant', 'ramp']
algos = ['kube-scheduler', 'kse-GreedyLB', 'kse-RefineLB']
executions = ['results_1', 'results_2', 'results_3', 'results_4']

def save_grouped_graphics(distribution, metric):
  executions_data = defaultdict(dict)
  for execution in executions:
    csv_reader = csv.reader(open(execution + '/results.csv'), delimiter=',')
    for row in csv_reader:
      executions_data[execution+'_'+row[0]][row[1]] = row[2]

  scenarios = []
  mae_data = {'kube-scheduler': [], 'kse-GreedyLB': [], 'kse-RefineLB': []}
  std_data = {'kube-scheduler': [], 'kse-GreedyLB': [], 'kse-RefineLB': []}
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
              data_array = []
              for execution in executions:
                data_array.append(float(executions_data[execution+'_'+key][algo]))
              mae_data[algo].append(round(np.mean(data_array), 2))
              std_data[algo].append(round(np.std(data_array), 2))
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
      std = std_data[attribute]
      rects = ax.bar(x + offset, measurement, width, yerr=std, capsize=5, label=attribute)
      ax.bar_label(rects, padding=2, rotation=90)
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
    plt.savefig('grouped_mean_'+distribution+'_'+metric+'.svg', dpi=150, transparent=False, bbox_inches='tight', format='svg')
  except Exception as error:
    print(error)
  finally:
    plt.close()
    plt.cla()
    plt.clf()

save_grouped_graphics('normal', 'memory')
save_grouped_graphics('normal', 'cpu')
save_grouped_graphics('exponential', 'memory')
save_grouped_graphics('exponential', 'cpu')
