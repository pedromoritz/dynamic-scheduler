#!/usr/bin/env python3

import kse as kse
import numpy as np

def scheduling_workflow():
  cluster = kse.Cluster()
  nodes = cluster.get_nodes()
  pending_pods = cluster.get_pending_pods()
  nodes_sequence = []
  allocation_plan = {}
  for i in range(int(len(pending_pods) / len(nodes))):
    np.random.shuffle(nodes)
    nodes_sequence+=nodes
  for j in range(len(pending_pods)):
    allocation_plan[pending_pods[j]['name']] = nodes_sequence[j]['name'] 
  cluster.set_allocation_plan(allocation_plan)

scheduling_workflow()

