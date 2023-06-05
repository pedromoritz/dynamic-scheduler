#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

def save_graphic(value1, value2, value3, metric, filename):
  if metric == 'memory':
    plt.ylim(0, 500)
    plt.ylabel('memory (MB)')
  if metric == 'cpu':
    plt.ylim(0, 200)
    plt.ylabel('CPU (millicpu)')
#  plt.bar(0, value1, label='kube-scheduler')
#  plt.bar(1, value2, label='kse + GreedyLB')
#  plt.bar(2, value3, label='kse + RefineLB')
  plt.legend(loc="upper left")

  x = np.arange(1)
  y1 = [34, 56, 12, 89, 67]
  y2 = [12, 56, 78, 45, 90]
  y3 = [14, 23, 45, 25, 89]
  width = 0.2
  
  plt.bar(x-0.2, y1, width, color='cyan')
  plt.bar(x, y2, width, color='orange')
  plt.bar(x+0.2, y3, width, color='green')
  plt.xticks(x, ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'])
#  plt.legend(["Round 1", "Round 2", "Round 3"])
  plt.savefig('results/'+filename, dpi=400, transparent=False, bbox_inches='tight')
  plt.close()
  plt.cla()
  plt.clf()

save_graphic(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

