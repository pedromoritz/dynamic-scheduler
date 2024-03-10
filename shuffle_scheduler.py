#!/usr/bin/env python3

import kse as kse
import numpy as np

def scheduling_workflow():
  cluster = kse.Cluster()
  pending_pods = cluster.get_pending_pods()
  distribution_array=['ppgcc-m05', 'ppgcc-m03', 'ppgcc-m02', 'ppgcc-m04', 'ppgcc-m05', 'ppgcc-m03', 'ppgcc-m02', 'ppgcc-m04', 'ppgcc-m03', 'ppgcc-m05', 'ppgcc-m04', 'ppgcc-m02', 'ppgcc-m02', 'ppgcc-m03', 'ppgcc-m05', 'ppgcc-m04', 'ppgcc-m03', 'ppgcc-m04', 'ppgcc-m05', 'ppgcc-m02', 'ppgcc-m05', 'ppgcc-m03', 'ppgcc-m02', 'ppgcc-m04', 'ppgcc-m05', 'ppgcc-m03', 'ppgcc-m02', 'ppgcc-m04', 'ppgcc-m03', 'ppgcc-m05', 'ppgcc-m04', 'ppgcc-m02', 'ppgcc-m02', 'ppgcc-m03', 'ppgcc-m05', 'ppgcc-m04', 'ppgcc-m03', 'ppgcc-m04', 'ppgcc-m05', 'ppgcc-m02']
  allocation_plan = {}
  for j in range(len(pending_pods)):
    allocation_plan[pending_pods[j]['name']] = distribution_array[j]
  cluster.set_allocation_plan(allocation_plan)

scheduling_workflow()

