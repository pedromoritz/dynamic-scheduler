#!/usr/bin/env python3

import json
import dynamic_scheduler_core as dscore

cluster = dscore.Cluster()

for node_item in cluster.nodes:
	print('-------------')
	print(node_item)
	node = dscore.Node(node_item['name'])
	print(node.metrics)

#print(json.dumps(cluster.nodes))