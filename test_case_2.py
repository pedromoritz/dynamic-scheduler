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

  all_pods = []

  for node_item in nodes:
    node = dscore.Node(node_item['name'], namespace)
    print('---> Buscando metricas para o node ' + node_item['name'] + ':')
    print(node.metrics)
    print('')
    node_item['usage'] = node.metrics['usage']

    print('---> Buscando pods do node ' + node_item['name'] + ':')
    node = dscore.Node(node_item['name'], namespace)
    pods_temp = node.pods
    print(pods_temp)
    print('')

    for pod_temp in pods_temp:
      all_pods.append(pod_temp)

  allocation = []
  print('---> Criando uma lista de alocação')
  for item in all_pods:
    allocation.append({
      'name': item['name'],
      'namespace': item['namespace'],
      'node': 'ppgcc-m03' # AQUI VAI O CRITÉRIO DE ALOCAÇÃO
    })

  cluster.set_allocation(allocation)

# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(scheduling_workflow, 'interval', seconds=5)
scheduler.start()

# keeping script running
while True:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    scheduler.shutdown()
    break
