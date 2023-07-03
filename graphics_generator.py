#!/usr/bin/env python3

import os
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pylab import cm
import sys
from collections.abc import Iterable

def get_standard_deviation(dataset):
  data_list = []
  for data in dataset:
    data_list.append(round(np.average(data), 2))
  sorted_data_list = sorted(data_list)
  min_value = sorted_data_list[0]
  max_value = sorted_data_list[-1]
  mean = sum(data_list) / len(data_list)
  variance = sum([((x - mean) ** 2) for x in data_list]) / len(data_list)
  standard_deviation = round(variance ** 0.5, 2)
  return [min_value, max_value, round(mean, 2), standard_deviation]

def save_graphic(timestamp, data1, data2, data3, data4, xlabel, ylim, ylabel, final_filename, migrations):
  plt.xlim(0, 600)
  plt.xlabel(xlabel)
  plt.ylim(0, ylim)
  plt.ylabel(ylabel)
  plt.plot(timestamp, data1, label='node 1', linewidth='2')
  plt.plot(timestamp, data2, label='node 2', linewidth='2')
  plt.plot(timestamp, data3, label='node 3', linewidth='2')
  plt.plot(timestamp, data4, label='node 4', linewidth='2')
  if isinstance(migrations, Iterable):
    for migration in migrations:
      plt.axvline(x = migration, color = 'red', linewidth='0.7', linestyle='dashed')
  plt.legend(loc="upper left")
  print("Generating " + final_filename)
  dataset = []
  dataset.append(data1)
  dataset.append(data2)
  dataset.append(data3)
  dataset.append(data4)
  plt.axhline(y = get_standard_deviation(dataset)[2], color = 'gray', linewidth='0.7')
  plt.savefig(final_filename, dpi=400, transparent=False, bbox_inches='tight')
  plt.legend(loc="upper left")
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
      xlabel = 'time (s)'
      ylim = 2048
      ylabel = 'memory (MB)'
    elif 'cpu' in FILE_NAME:
      # generating cpu graphics
      data1 = list(map(lambda n: n/1000000, n1_cpu))
      data2 = list(map(lambda n: n/1000000, n2_cpu))
      data3 = list(map(lambda n: n/1000000, n3_cpu))
      data4 = list(map(lambda n: n/1000000, n4_cpu))
      xlabel = 'time (s)'
      ylim = 2000
      ylabel = 'CPU (millicpu)'
    final_filename = FILE_NAME + '.png'
    MIGRATIONS_FILE_NAME = FILE_NAME.replace('metrics', 'migrations')
    if os.path.isfile(MIGRATIONS_FILE_NAME + '.csv'):
      migrations = np.loadtxt(MIGRATIONS_FILE_NAME + '.csv', unpack=True, delimiter=',', skiprows=0, usecols=[0], ndmin=1)
    save_graphic(timestamp, data1, data2, data3, data4, xlabel, ylim, ylabel, final_filename, migrations)
  except Exception:
    print('error ---> ' + FILE_NAME + '.csv')

