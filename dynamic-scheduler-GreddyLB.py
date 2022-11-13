#!/usr/bin/env python3

import json
import time
import k8s_helper_core as khc
from apscheduler.schedulers.background import BackgroundScheduler

namespace = 'lab'

# workflow definitions
def scheduling_workflow():
  print('##########################################')
  print('Iniciando workflow', end="\n\n")

  cluster = khc.Cluster()
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
  print('absolute delta: ' + str(absolute_delta) + 'KB | ' + 'percentual delta: ' + str(percentual_delta) + '%', end="\n\n")

  if (percentual_delta > 10):

    all_pods = []

    for node_item in nodes:
      print('---> Buscando pods do node ' + node_item['name'] + ':')
      node = khc.Node(node_item['name'], namespace)
      pods_temp = node.pods

      for pod_temp in pods_temp:
        pod_temp['source_node'] = node_item['name']
        all_pods.append(pod_temp)
        print(pod_temp)

      print('')

    allocation_plan = []
    print('---> Criando uma lista de alocação')

    rr_counter = 0
    for pod in all_pods:
      allocation_plan.append({
        'pod_name': pod['name'],
        'namespace': pod['namespace'],
        'target_node': nodes[rr_counter]['name']
      })
      rr_counter = rr_counter + 1 if rr_counter < len(nodes) - 1 else 0

    for allocation_plan_item in allocation_plan:
      print(allocation_plan_item)

    cluster.set_allocation_plan(allocation_plan)

# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(scheduling_workflow, 'interval', seconds=30)
scheduler.start()

# keeping script running
while True:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    scheduler.shutdown()
    break
