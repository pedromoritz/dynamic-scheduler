#!/usr/bin/env python3

import dynamic_scheduler_core as dscore

namespace = 'lab'

def scheduling_workflow():
  cluster = dscore.Cluster()
  nodes = cluster.nodes
  pending_pods = cluster.pending_pods

  allocation_plan = []
  rr_counter = 0

  for pod in pending_pods:
    target_node = nodes[rr_counter]['name'] # ROUND ROBIN
    if rr_counter < len(nodes) - 1: 
      rr_counter =+ 1 
    else: 
      rr_counter = 0

    allocation_plan.append({
      'pod_name': pod['name'],
      'namespace': pod['namespace'],
      'target_node': target_node
    })
  print(allocation_plan)
  cluster.set_allocation_plan(allocation_plan)

scheduling_workflow()
