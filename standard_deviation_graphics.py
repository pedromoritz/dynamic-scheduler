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
  Gender=['Male','Female']
  pos = np.arange(len(city))
  bar_width = 0.35
  Happiness_Index_Male=[60,40,70,65,85]
  Happiness_Index_Female=[30,60,70,55,75]
 
  plt.bar(pos,Happiness_Index_Male,bar_width,color='blue',edgecolor='black')
  plt.bar(pos+bar_width,Happiness_Index_Female,bar_width,color='pink',edgecolor='black')
  plt.xticks(pos, city)
  plt.xlabel('City', fontsize=16)
  plt.ylabel('Happiness_Index', fontsize=16)
  plt.title('Group Barchart - Happiness index across cities By Gender',fontsize=18)
  plt.legend(Gender,loc=2)

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

