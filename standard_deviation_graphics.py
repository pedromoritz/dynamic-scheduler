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
  plt.bar('kube-scheduler', value1)
  plt.bar('kse + GreedyLB', value2)
  plt.bar('kse + RefineLB', value3)
  plt.legend(loc="upper left")
  plt.savefig(filename, dpi=400, transparent=False, bbox_inches='tight')
  plt.close()
  plt.cla()
  plt.clf()

#  x = np.array(['kube-scheduler', 'kse + GreedyLB', 'kse + RefineLB'])
#  y = np.array([value1, value2, value3])
#  plt.bar(x,y)
#  plt.savefig('results/'+filename, dpi=400, transparent=False, bbox_inches='tight')
#  plt.legend(loc="upper left")
#  plt.close()
#  plt.cla()
#  plt.clf()

save_graphic(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

