#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

def addlabels(x,y):
  for i in range(len(x)):
    plt.text(i, y[i], y[i], ha = 'center')

def save_graphic(value1, value2, value3, metric, filename):
  if metric == 'memory':
    plt.ylim(0, 200)
    plt.ylabel('memory (MB)')
  elif metric == 'cpu':
    plt.ylim(0, 500)
    plt.ylabel('CPU (millicpu)')

  x = ['kube-scheduler', 'kse + GreedyLB', 'kse + RefineLB']
  y = [value1, value2, value3]

  plt.bar(x, y)
  addlabels(x, y)
  plt.legend(loc="upper left")
  plt.savefig('results/'+filename, dpi=400, transparent=False, bbox_inches='tight')
  plt.close()
  plt.cla()
  plt.clf()

save_graphic(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5])

