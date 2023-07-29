#!/usr/bin/env python3

import kse as kse
import numpy as np

def scheduling_workflow():
  cluster = kse.Cluster()
  pending_pods = cluster.get_pending_pods()
  nodes = ['ppgcc-m02', 'ppgcc-m03', 'ppgcc-m04', 'ppgcc-m05']
  shuffle_sequence = [0, 0, 1, 0, 1, 3, 2, 0, 1, 1, 0, 2, 3, 1, 3, 2, 2, 3, 2, 3, 0, 0, 1, 0, 1, 3, 2, 0, 1, 1, 0, 2, 3, 1, 3, 2, 2, 3, 2, 3]
  allocation_plan = {}
  for j in range(len(pending_pods)):
    allocation_plan[pending_pods[j]['name']] = nodes[shuffle_sequence[j]]
  cluster.set_allocation_plan(allocation_plan)

scheduling_workflow()

