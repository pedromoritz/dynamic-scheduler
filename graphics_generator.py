#!/usr/bin/env python3

import os
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pylab import cm
import sys

for path in Path("results/").glob("metrics_*.csv"):
  FILE_NAME, FILE_EXTENSION = os.path.splitext(path)
  print("Reading " + str(path))
  timestamp, m_node1, pa_node1, m_node2, pa_node2, m_node3, pa_node3 = np.loadtxt(FILE_NAME + '.csv', unpack=True, delimiter=',', skiprows=1)
  m_node1_mb = list(map(lambda n: n/1024, m_node1))
  m_node2_mb = list(map(lambda n: n/1024, m_node2))
  m_node3_mb = list(map(lambda n: n/1024, m_node3))

  plt.xlabel('time (s)')
  plt.ylim(0, 4096)
  plt.ylabel('memory (MB)')
  plt.plot(timestamp, m_node1_mb, label='node 1', linewidth='2')
  plt.plot(timestamp, m_node2_mb, label='node 2', linewidth='2')
  plt.plot(timestamp, m_node3_mb, label='node 3', linewidth='2')
  
  if 'kse' in FILE_NAME:
    MIGRATIONS_FILE_NAME = FILE_NAME.replace('metrics', 'migrations')
    timestamps, pod, source_node, target_node = np.loadtxt(MIGRATIONS_FILE_NAME + '.csv', unpack=True, delimiter=',', skiprows=0)  
    for ts in timestamps:
      plt.axvline(x = ts, color = 'red', linewidth='1', linestyle='dashed')

  plt.legend(loc="upper left")
  print("Generating " + FILE_NAME + ".png")
  plt.savefig(FILE_NAME + '.png', dpi=400, transparent=False, bbox_inches='tight')
  plt.legend(loc="upper left")
  plt.close()
  plt.cla()
  plt.clf()
