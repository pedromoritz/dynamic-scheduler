#!/usr/bin/env python3

import os
from pathlib import Path
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from bs4 import BeautifulSoup
import csv

lang = 'pt' 
normalStr = 'normal' if lang == 'pt' else 'normal'
exponentialStr = 'exponencial' if lang == 'pt' else 'exponential'
availabilityStr = 'Disponibilidade' if lang == 'pt' else 'Availability'

pods = [10, 20]
targets = [20, 40]
rates = ['constant', 'ramp']
distributions = ['exponential', 'normal']
metrics = ['memory', 'cpu']
algos = ['kube-scheduler', 'kse-GreedyLB', 'kse-RefineLB']
executions = ['results_1', 'results_2', 'results_3', 'results_4', 'results_5', 'results_6', 'results_7', 'results_8', 'results_9', 'results_10']

def save_grouped_graphics(rate, metric):
  executions_data = defaultdict(dict)
  scenarios = []
  ava_data = {'kube-scheduler': [], 'kse-GreedyLB': [], 'kse-RefineLB': []}
  std_data = {'kube-scheduler': [], 'kse-GreedyLB': [], 'kse-RefineLB': []}
  for distribution in distributions:
    for target in targets:
      for pod in pods:
        key = str(pod) + '_' + str(target) + '_' + rate + '_' + distribution + '_' + metric
        if distribution == 'normal':
          scenarios.append(str(pod)+' pods\n'+str(target)+' req/s\n'+normalStr)
        elif distribution == 'exponential': 
          scenarios.append(str(pod)+' pods,\n'+str(target)+' req/s\n'+exponentialStr)  
        for algo in algos:
          data_array = []
          for execution in executions:
            try:
              obj_requests = get_requests_count(execution, algo+'_'+key)  
              data_total = float(obj_requests['total'])
              data_failed = float(obj_requests['failed'])
              data_array.append((data_total - data_failed) / ((data_total - data_failed) + data_failed) * 100)
            except Exception as error:
              data_array.append(100)
          ava_data[algo].append(round(np.mean(data_array), 2))
          std_data[algo].append(round(np.std(data_array), 2))

  x = np.arange(len(scenarios))
  width = 0.25
  multiplier = 0
  plt.figure().set_figwidth(12)
  fig, ax = plt.subplots(figsize=(14,3.1))
  try:
    for attribute, measurement in ava_data.items():
      offset = width * multiplier
      std = std_data[attribute]
      rects = ax.bar(x + offset, measurement, width, yerr=std, capsize=5, label=attribute)
      multiplier += 1
    if rate == 'constant':
      ax.set_ylim(20, 101)
    elif rate == 'ramp': 
      ax.set_ylim(90, 101)
    ax.set_ylabel(availabilityStr, fontsize=12)
    ax.set_xticks(x + width, scenarios, fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ksl = mpatches.Patch(color='#1f77b4', label='Kube-Scheduler')
    ksegl = mpatches.Patch(color='#ff7f0e', label='KSE-GreedyLB')
    kserl = mpatches.Patch(color='#2ca02c', label='KSE-RefineLB')
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    if rate == 'constant':
      ax.legend(handles=[ksl, ksegl, kserl], loc='upper right', fontsize=12)
    elif rate == 'ramp':
      ax.legend(handles=[ksl, ksegl, kserl], loc='lower right', fontsize=12)
    plt.savefig('grouped_mean_availability_'+rate+'_'+metric+'.svg', dpi=150, transparent=False, bbox_inches='tight', format='svg')
  except Exception as error:
    print(error)
  finally:
    plt.close()
    plt.cla()
    plt.clf()

def get_requests_count(execution, filename):
  try:
    with open(execution + '/summary_'+filename+'.html', 'r') as fp:
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

save_grouped_graphics('constant', 'memory')
save_grouped_graphics('constant', 'cpu')
save_grouped_graphics('ramp', 'memory')
save_grouped_graphics('ramp', 'cpu')

