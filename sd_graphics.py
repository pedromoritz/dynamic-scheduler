#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

def addlabels(x,y):
  for i in range(len(x)):
    plt.text(i, y[i]+5, y[i], ha = 'center')

def save_graphic(value1, value2, value3, filename):
  if 'memory' in filename:
    plt.ylim(0, 200)
    plt.ylabel('memory (MB)')
  elif 'cpu' in filename:
    plt.ylim(0, 500)
    plt.ylabel('CPU (millicpu)')
  x = ['kube-scheduler', 'KSE+GreedyLB', 'KSE+RefineLB']
  y = [value1, value2, value3]
  plt.bar(x, y)
  addlabels(x, y)
  #plt.axes().yaxis.grid()
  plt.savefig('results/'+filename, dpi=400, transparent=False, bbox_inches='tight')
  plt.close()
  plt.cla()
  plt.clf()

if len(sys.argv) == 5:
  save_graphic(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
else:
  print("usage: ./sd_graphics.sh <kube-scheduler> <KSE+GreedyLB> <KSE+RefineLB> <FILENAME>")
