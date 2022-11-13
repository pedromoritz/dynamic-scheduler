#!/usr/bin/env python3

import k8s_helper_core as khc

namespace = 'lab'

def scheduling_workflow():
  cluster = khc.Cluster()
  nodes = cluster.nodes
  pending_pods = cluster.pending_pods
  allocation_plan = []
  rr_counter = 0
  for pod in pending_pods:
    allocation_plan.append({
      'pod_name': pod['name'],
      'namespace': pod['namespace'],
      'target_node': nodes[rr_counter]['name']
    })
    rr_counter = rr_counter + 1 if rr_counter < len(nodes) - 1 else 0
  cluster.set_allocation_plan(allocation_plan)

scheduling_workflow()
