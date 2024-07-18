#!/usr/bin/env python3

import os
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pylab import cm
import sys
from collections.abc import Iterable

lang = 'pt' 
timeStr = 'tempo' if lang == 'pt' else 'time'
memoryStr = 'memória' if lang == 'pt' else 'memory'
nodeStr = 'nó' if lang == 'pt' else 'node'

def save_load_graphic(timestamp, data1, data2, data3, data4, xlabel, ylim, ylabel, final_filename, migrations):
  plt.xlim(0, 600)
  plt.xlabel(xlabel, fontsize=18)
  plt.xticks(fontsize=16)
  plt.ylim(0, ylim)
  plt.ylabel(ylabel, fontsize=18)
  plt.yticks(fontsize=16)
  title = ''
  if 'kube-scheduler' in final_filename:
    title = 'Kube-Scheduler'
  elif 'kse-GreedyLB' in final_filename:
    title = 'KSE-GreedyLB'
  elif 'kse-RefineLB' in final_filename:
    title = 'KSE-RefineLB'
  plt.title(title, fontsize=18, fontweight='bold')
  plt.plot(timestamp, data1, label=nodeStr+' 1', linewidth='2')
  plt.plot(timestamp, data2, label=nodeStr+' 2', linewidth='2')
  plt.plot(timestamp, data3, label=nodeStr+' 3', linewidth='2')
  plt.plot(timestamp, data4, label=nodeStr+' 4', linewidth='2')
  previousMigration = 0
  if isinstance(migrations, Iterable):
    for migration in migrations:
      if previousMigration == 0 or previousMigration != migration:
        plt.axvline(x = migration, color = 'red', linewidth='0.5', linestyle=(0, (5, 1)))
        previousMigration = migration
  plt.legend(loc="lower right", fontsize=16)
  print("Generating " + final_filename)
  dataset = []
  dataset.append(data1)
  dataset.append(data2)
  dataset.append(data3)
  dataset.append(data4)
  plt.savefig(final_filename, dpi=150, transparent=False, bbox_inches='tight', format='svg')
  plt.close()
  plt.cla()
  plt.clf()

for path in Path("results/").glob("metrics_*.csv"):
  FILE_NAME, FILE_EXTENSION = os.path.splitext(path)
  print("Reading " + str(path))
  try:
    timestamp, n1_pod_amount, n1_memory, n1_cpu, n2_pod_amount, n2_memory, n2_cpu, n3_pod_amount, n3_memory, n3_cpu, n4_pod_amount, n4_memory, n4_cpu = np.loadtxt(FILE_NAME + '.csv', unpack=True, delimiter=',', skiprows=1, ndmin=1)
    migrations = []
    if 'memory' in FILE_NAME:
      # generating memory graphics
      data1 = list(map(lambda n: n/1024, n1_memory))
      data2 = list(map(lambda n: n/1024, n2_memory))
      data3 = list(map(lambda n: n/1024, n3_memory))
      data4 = list(map(lambda n: n/1024, n4_memory))
      xlabel = timeStr+' (s)'
      ylim = 2048
      ylabel = memoryStr+' (MB)'
    elif 'cpu' in FILE_NAME:
      # generating cpu graphics
      data1 = list(map(lambda n: n/1000000, n1_cpu))
      data2 = list(map(lambda n: n/1000000, n2_cpu))
      data3 = list(map(lambda n: n/1000000, n3_cpu))
      data4 = list(map(lambda n: n/1000000, n4_cpu))
      xlabel = timeStr+' (s)'
      ylim = 2000
      ylabel = 'CPU (millicpu)'
    final_filename = FILE_NAME + '.svg'
    MIGRATIONS_FILE_NAME = FILE_NAME.replace('metrics', 'migrations')
    if os.path.isfile(MIGRATIONS_FILE_NAME + '.csv'):
      migrations = np.loadtxt(MIGRATIONS_FILE_NAME + '.csv', unpack=True, delimiter=',', skiprows=0, usecols=[0], ndmin=1)
    save_load_graphic(timestamp, data1, data2, data3, data4, xlabel, ylim, ylabel, final_filename, migrations)
  except Exception:
    print('error ---> ' + FILE_NAME + '.csv')

