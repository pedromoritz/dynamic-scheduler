#!/usr/bin/env python3

import matplotlib.pyplot as plt
import math
import numpy as np

x = np.loadtxt('requests.csv', unpack=True, delimiter=',', skiprows=0)
plt.hist(x, 100, histtype = 'bar')
xint = range(int(max(x)+1))
plt.xticks(xint)
plt.savefig('requests.png', dpi=400, transparent=False, bbox_inches='tight')
plt.close()

