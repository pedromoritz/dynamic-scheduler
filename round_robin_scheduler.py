#!/usr/bin/env python3

import k8s_scheduling_extension as kse

def scheduling_workflow():
  cluster = kse.Cluster()
  nodes = cluster.nodes
  pending_pods = cluster.pending_pods
  allocation_plan = {}
  rr_counter = 0
  for pod in pending_pods:
    allocation_plan[pod['name']] = nodes[rr_counter]['name'] 
    rr_counter = rr_counter + 1 if rr_counter < len(nodes) - 1 else 0
  cluster.set_allocation_plan(allocation_plan)

scheduling_workflow()
