#!/usr/bin/env python3

import json
import dynamic_scheduler_core as dscore

cluster = dscore.Cluster()
nodes = cluster.nodes

for node_item in nodes:
  node = dscore.Node(node_item['name'])
  #print("metricas")
  #print(node.metrics)
  #print("depois")
  node_item['usage'] = node.metrics['usage']
  #print(node_item)

nodes_sorted_by_used_memory = sorted(nodes, key=lambda d: d['usage']['memory'])

node_more_used_memory = nodes_sorted_by_used_memory[-1]

print(node_more_used_memory['name'])

node = dscore.Node(node_more_used_memory['name'])
print(node.pods)