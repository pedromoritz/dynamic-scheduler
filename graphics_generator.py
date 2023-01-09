#!/usr/bin/env python3

# Import required packages
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pylab import cm

CSV_FILENAME = 'metrics_dynamic_scheduler_GreedyLB_6_pods.csv'

#timestamp,ppgcc-m02,ppgcc-m02_pods,ppgcc-m03,ppgcc-m03_pods,ppgcc-m04,ppgcc-m04_pods

timestamp, node1 = np.loadtxt(CSV_FILENAME, unpack=True, delimiter=',', skiprows=1)

#def to_relative_time(n):
#  return n - timestamp[0]

#relative_time = list(map(to_relative_time, timestamp))
#plt.plot(timestamp, node1)
#plt.savefig('Final_Plot.png', dpi=300, transparent=False, bbox_inches='tight')
