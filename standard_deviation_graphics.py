#!/usr/bin/env python3

import os
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pylab import cm
import sys

def save_graphic(value1, value2, value3, metric, filename):
  if metric == 'memory':
    plt.ylim(0, 500)
    plt.ylabel('memory (MB)')
  if metric == 'cpu':
    plt.ylim(0, 200)
    plt.ylabel('CPU (millicpu)')
  plt.bar(0, value1, label='kube-scheduler')
  plt.bar(0, value2, label='kse + GreedyLB')
  plt.bar(0, value3, label='kse + RefineLB')
  plt.legend(loc="upper left")
  plt.savefig('results/'+filename, dpi=400, transparent=False, bbox_inches='tight')
  plt.close()
  plt.cla()
  plt.clf()

save_graphic(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

