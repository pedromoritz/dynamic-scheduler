#!/usr/bin/env python3

import os
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pylab import cm
import sys

def save_graphic(value1, value2, value3, metric, filename):
 # if metric == 'memory':
  #  plt.ylim(0, 500)
 #   plt.ylabel('memory (MB)')
 # if metric == 'cpu':
  #  plt.ylim(0, 200)
 #   plt.ylabel('CPU (millicpu)')
#  plt.bar('', value1, label='kube-scheduler')
#  plt.bar('', value2, label='kse + GreedyLB')
#  plt.bar('', value3, label='kse + RefineLB')
  #plt.legend(loc="upper left")
#  plt.savefig('results/'+filename, dpi=400, transparent=False, bbox_inches='tight')
#  plt.close()
#  plt.cla()
#  plt.clf()

  city=['Delhi','Beijing','Washington','Tokyo','Moscow']
  scheduler=['kube-scheduler', 'kse + GreedyLB', 'kse + RefineLB']
  pos = np.arange(len(city))
  Happiness_Index_Male=[60,40,70,65,85]
  Happiness_Index_Female=[30,60,70,55,75]
 
  plt.bar(1, value1)
  plt.bar(2, value2)
  plt.bar(3, value3)
  plt.xticks(pos, city)
  plt.xlabel('City', fontsize=16)
  plt.ylabel('Happiness_Index', fontsize=16)
  plt.legend(scheduler, loc='upper left')
  plt.savefig('results/'+filename, dpi=400, transparent=False, bbox_inches='tight')
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

