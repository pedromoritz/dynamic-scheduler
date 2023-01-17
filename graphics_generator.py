#!/usr/bin/env python3

# Import required packages
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pylab import cm
import sys

TEST_NAME = sys.argv[1]

timestamp, m_node1, pa_node1, m_node2, pa_node2, m_node3, pa_node3 = np.loadtxt(TEST_NAME + '.csv', unpack=True, delimiter=',', skiprows=1)

m_node1_mb = list(map(lambda n: n/1024, m_node1))
m_node2_mb = list(map(lambda n: n/1024, m_node2))
m_node3_mb = list(map(lambda n: n/1024, m_node3))

plt.xlabel('time (s)')
plt.ylim(0, 4096)
plt.ylabel('memory (MB)')
plt.plot(timestamp, m_node1_mb, label='node 1')
plt.plot(timestamp, m_node2_mb, label='node 2')
plt.plot(timestamp, m_node3_mb, label='node 3')
plt.savefig(TEST_NAME + '.png', dpi=300, transparent=False, bbox_inches='tight')
