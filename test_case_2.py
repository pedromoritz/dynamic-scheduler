#!/usr/bin/env python3

import json
import time
import dynamic_scheduler_core as dscore
from apscheduler.schedulers.background import BackgroundScheduler

namespace = 'lab'

# workflow definitions
def scheduling_workflow():
  print('##########################################')
  print('Iniciando workflow', end="\n\n")

  cluster = dscore.Cluster()
  print('---> Buscando nodes do cluster:')
  nodes = cluster.nodes

  for node_item in nodes:
    print(node_item)
  print('')

  print('---> Buscando node com maior uso absoluto de memória:')
  nodes_sorted_by_used_memory = sorted(nodes, key=lambda d: d['usage']['memory'])
  node_more_used_memory = nodes_sorted_by_used_memory[-1]
  print(node_more_used_memory, end="\n\n")

  print('---> Buscando node com menor uso absoluto de memória:')
  nodes_sorted_by_used_memory_reverse = sorted(nodes, key=lambda d: d['usage']['memory'], reverse=True)
  node_less_used_memory = nodes_sorted_by_used_memory_reverse[-1]
  print(node_less_used_memory, end="\n\n")

  print('---> Verificando se a diferença entre os nodes selecionados é maior que 10% da capacidade máxima:')
  absolute_delta = (node_more_used_memory['usage']['memory'] - node_less_used_memory['usage']['memory'])
  percentual_delta = round((absolute_delta / node_more_used_memory['capacity']['memory']) * 100, 2)
  print('absolute delta: ' + str(absolute_delta) + ' | ' + 'percentual delta: ' + str(percentual_delta) + '%', end="\n\n")

  if (percentual_delta > 10):

    all_pods = []

    for node_item in nodes:
      print('---> Buscando pods do node ' + node_item['name'] + ':')
      node = dscore.Node(node_item['name'], namespace)
      pods_temp = node.pods

      for pod_temp in pods_temp:
        pod_temp['source_node'] = node_item['name']
        all_pods.append(pod_temp)
        print(pod_temp)

      print('')

    allocation_plan = []
    print('---> Criando uma lista de alocação')
    for item in all_pods:
      allocation_plan.append({
        'name': item['name'],
        'namespace': item['namespace'],
        'source_node': item['source_node'],
        'target_node': node_less_used_memory['name'] # AQUI VAI O CRITÉRIO DE ALOCAÇÃO
      })

    for allocation_plan_item in allocation_plan:
      print(allocation_plan_item)

    cluster.set_allocation_plan(allocation_plan)

scheduling_workflow()

# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(scheduling_workflow, 'interval', seconds=60)
scheduler.start()

# keeping script running
while True:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    scheduler.shutdown()
    break
