#!/usr/bin/env python3

import kse as kse

def scheduling_workflow():
  cluster = kse.Cluster()
  nodes = cluster.get_nodes()
  pending_pods = cluster.get_pending_pods()
  allocation_plan = {}
  counter = 0
  for pod in pending_pods:
    allocation_plan[pod['name']] = nodes[counter]['name'] 
  #  rr_counter = rr_counter + 1 if rr_counter < len(nodes) - 1 else 0
  #cluster.set_allocation_plan(allocation_plan)
  print(allocation_plan)

scheduling_workflow()
