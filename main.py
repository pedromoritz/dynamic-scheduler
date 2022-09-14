#!/usr/bin/env python3

import json
import time
import dynamic_scheduler_core as dscore
from apscheduler.schedulers.background import BackgroundScheduler

namespace = 'lab'

# workflow definitions
def scheduling_workflow():
  print('##########################################')
  print('Iniciando workflow')
  print('')

  cluster = dscore.Cluster()
  print('---> Buscando nodes do cluster:')
  nodes = cluster.nodes
  print(nodes)
  print('')

  for node_item in nodes:
    node = dscore.Node(node_item['name'], namespace)
    print('---> Buscando metricas para o node ' + node_item['name'] + ':')
    print(node.metrics)
    print('')
    node_item['usage'] = node.metrics['usage']

  print('---> Nodes com respectivas metricas:')
  print(nodes)
  print('')

  print('---> Buscando node com maior uso absoluto de memória:')
  nodes_sorted_by_used_memory = sorted(nodes, key=lambda d: d['usage']['memory'])
  node_more_used_memory = nodes_sorted_by_used_memory[-1]
  print(node_more_used_memory)
  print('')

  print('---> Buscando pods do node ' + node_more_used_memory['name'] + ':')
  node = dscore.Node(node_more_used_memory['name'], namespace)
  print(node.pods)

# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(scheduling_workflow, 'interval', seconds=10)
scheduler.start()

# keeping script running
while True:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    scheduler.shutdown()
    break
