#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

def save_graphic(value1, value2, value3, metric, filename):
  if metric == 'memory':
    plt.ylim(0, 500)
    plt.ylabel('memory (MB)')
  elif metric == 'cpu':
    plt.ylim(0, 200)
    plt.ylabel('CPU (millicpu)')

  x = np.arange(1)
  y1 = [value1]
  y2 = [value2]
  y3 = [value3]
  width = 0.2
  
  plt.bar(x-0.2, y1, width, label='kube-scheduler', color='cyan')
  plt.bar(x, y2, width, label='kse + GreedyLB', color='orange')
  plt.bar(x+0.2, y3, width, label='kse + RefineLB', color='green')
  plt.xticks(x, ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'])
  plt.legend(loc="upper left")
  plt.savefig('results/'+filename, dpi=400, transparent=False, bbox_inches='tight')
  plt.close()
  plt.cla()
  plt.clf()

save_graphic(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

