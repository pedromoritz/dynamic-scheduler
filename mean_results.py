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
distributions = ['exponential', 'normal']
metrics = ['memory', 'cpu']
algos = ['kube-scheduler', 'kse-GreedyLB', 'kse-RefineLB']
executions = ['results_1', 'results_2', 'results_3', 'results_4', 'results_5', 'results_6', 'results_7', 'results_8', 'results_9', 'results_10']

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
           scenarios.append(str(pod)+' pods,\n'+str(target)+' req/s\n'+'linear')  
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
      #ax.bar_label(rects, padding=2, rotation=90)
      multiplier += 1
    if metric == 'memory':
      ax.set_ylim(0, 250)
      ax.set_ylabel('Erro Médio Absoluto', fontsize=12)
    elif metric == 'cpu':
      ax.set_ylim(0, 700)
      ax.set_ylabel('Erro Médio Absoluto', fontsize=12)
    ax.set_xticks(x + width, scenarios, fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ksl = mpatches.Patch(color='#1f77b4', label='Kube-Scheduler')
    ksegl = mpatches.Patch(color='#ff7f0e', label='KSE-GreedyLB')
    kserl = mpatches.Patch(color='#2ca02c', label='KSE-RefineLB')
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.legend(handles=[ksl, ksegl, kserl], loc='upper right', fontsize=12)
    plt.savefig('grouped_mean_'+distribution+'_'+metric+'.svg', dpi=150, transparent=False, bbox_inches='tight', format='svg')
  except Exception as error:
    print(error)
  finally:
    plt.close()
    plt.cla()
    plt.clf()

def get_migrations_count(execution, filename):
  try:
    with open(execution + '/migrations_'+filename+'.csv', 'r') as fp:
      return len(fp.readlines())
  except Exception as error:
    return 0

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

def show_availability():
  for pod in pods:
    for target in targets:
      for rate in rates:
        for distribution in distributions:
          for metric in metrics:
            key = str(pod) + '_' + str(target) + '_' + rate + '_' + distribution + '_' + metric
            for algo in algos:
              try:
                mean_migrations = 0
                mean_total = 0
                mean_failed = 0
                data_migrations = []
                data_total = []
                data_failed = []
                for execution in executions:
                  data_migrations.append(float(get_migrations_count(execution, algo+'_'+key)))
                  obj_requests = get_requests_count(execution, algo+'_'+key)
                  data_total.append(float(obj_requests['total']))
                  data_failed.append(float(obj_requests['failed']))
                mean_migrations = round(np.mean(data_migrations), 2)
                mean_total = round(np.mean(data_total), 0)
                mean_failed = round(np.mean(data_failed), 0)
                print(key+','+str(mean_migrations)+','+str(mean_total)+','+str(mean_failed))
              except Exception as error:
                total = 0
                failed = 0
                print('0, 0, 0')

save_grouped_graphics('normal', 'memory')
save_grouped_graphics('normal', 'cpu')
save_grouped_graphics('exponential', 'memory')
save_grouped_graphics('exponential', 'cpu')

show_availability()
