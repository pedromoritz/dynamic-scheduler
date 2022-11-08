#!/usr/bin/env python3

import dynamic_scheduler_core as dscore

namespace = 'lab'

def scheduling_workflow():
  cluster = dscore.Cluster()
  nodes = cluster.nodes
  all_pods = []

  for node_item in nodes:
    node = dscore.Node(node_item['name'], namespace)
    pods_temp = node.pods
    for pod_temp in pods_temp:
      pod_temp['source_node'] = node_item['name']
      all_pods.append(pod_temp)

  allocation_plan = []
  rr_counter = 0

  for item in all_pods:
    target_node = nodes[rr_counter]['name'] # ROUND ROBIN
    if rr_counter < len(nodes) - 1: 
      rr_counter =+ 1 
    else: 
      rr_counter = 0

    allocation_plan.append({
      'name': item['name'],
      'namespace': item['namespace'],
      'source_node': item['source_node'],
      'target_node': target_node
    })

  cluster.set_allocation_plan(allocation_plan)

scheduling_workflow()
