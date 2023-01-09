#!/usr/bin/env python3

# Import required packages
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pylab import cm

CSV_FILENAME = 'metrics_dynamic_scheduler_GreedyLB_6_pods.csv'

#timestamp,ppgcc-m02,ppgcc-m02_pods,ppgcc-m03,ppgcc-m03_pods,ppgcc-m04,ppgcc-m04_pods

timestamp, m_node1, pa_node1, m_node2, pa_node2, m_node3, pa_node3 = np.loadtxt(CSV_FILENAME, unpack=True, delimiter=',', skiprows=1)

m_node1_mb = list(map(lambda n: n/1024, m_node1))
m_node2_mb = list(map(lambda n: n/1024, m_node2))
m_node3_mb = list(map(lambda n: n/1024, m_node3))

plt.xlabel('time (s)')
plt.ylim(0, 4096)
plt.ylabel('memory (MB)')
plt.plot(timestamp, m_node1_mb)
plt.plot(timestamp, m_node2_mb)
plt.plot(timestamp, m_node3_mb)
plt.savefig(CSV_FILENAME+'.png', dpi=300, transparent=False, bbox_inches='tight')
