#!/usr/bin/env python3

import kse as kse
import numpy as np

def scheduling_workflow():
  cluster = kse.Cluster()
  nodes = cluster.get_nodes()
  pending_pods = cluster.get_pending_pods()
  nodes_sequence = ['ppgcc-m03', 'ppgcc-m05', 'ppgcc-m02', 'ppgcc-m04', 'ppgcc-m04', 'ppgcc-m05', 'ppgcc-m03', 'ppgcc-m02', 'ppgcc-m05', 'ppgcc-m03', 'ppgcc-m04', 'ppgcc-m02', 'ppgcc-m03', 'ppgcc-m04', 'ppgcc-m02', 'ppgcc-m05', 'ppgcc-m03', 'ppgcc-m05', 'ppgcc-m02', 'ppgcc-m04', 'ppgcc-m03', 'ppgcc-m02', 'ppgcc-m04', 'ppgcc-m05', 'ppgcc-m03', 'ppgcc-m05', 'ppgcc-m02', 'ppgcc-m04', 'ppgcc-m05', 'ppgcc-m03', 'ppgcc-m02', 'ppgcc-m04', 'ppgcc-m04', 'ppgcc-m05', 'ppgcc-m03', 'ppgcc-m02', 'ppgcc-m02', 'ppgcc-m04', 'ppgcc-m03', 'ppgcc-m05']
  allocation_plan = {}
  for j in range(len(pending_pods)):
    allocation_plan[pending_pods[j]['name']] = nodes_sequence[j] 
  cluster.set_allocation_plan(allocation_plan)

scheduling_workflow()

