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
  #print('---> Buscando nodes do cluster:')
  nodes = cluster.nodes
  #print(nodes)
  #print('')

  for node_item in nodes:
    node = dscore.Node(node_item['name'], namespace)
    #print('---> Buscando metricas para o node ' + node_item['name'] + ':')
    #print(node.metrics)
    #print('')
    node_item['usage'] = node.metrics['usage']

  print('---> Nodes com respectivas metricas:')
  print(nodes)
  print('')

  print('---> Buscando node com maior uso absoluto de memória:')
  nodes_sorted_by_used_memory = sorted(nodes, key=lambda d: d['usage']['memory'])
  node_more_used_memory = nodes_sorted_by_used_memory[-1]
  print(node_more_used_memory)
  print('')

  print('---> Verificando se o node selecionado possui ao menos 90% de uso de memória:')
  percentual_memory_usage = (node_more_used_memory['usage']['memory'] / node_more_used_memory['capacity']['memory']) * 100
  print(str(round(percentual_memory_usage, 2)) + '%')

  if percentual_memory_usage >= 90:

    print('---> Buscando pods do node ' + node_more_used_memory['name'] + ':')
    node = dscore.Node(node_more_used_memory['name'], namespace)
    print(node.pods)
    print('')

    print('---> Verifica Se há ao menos um pod no node selecionado:')
    print('')
    if len(node.pods) > 0: 

      print('---> Buscando primeiro pod da lista:')
      pod_to_evict = node.pods[0]
      print(pod_to_evict)
      print('')

      print('---> Despejando pod ' + pod_to_evict['name'] + ' do respectivo node:')
      pod = dscore.Pod(pod_to_evict['name'], pod_to_evict['namespace'])
      pod.evict()
      print('')

      print('---> Buscando node com menor uso absoluto de memória:')
      nodes_sorted_by_used_memory_reverse = sorted(nodes, key=lambda d: d['usage']['memory'], reverse=True)
      node_less_used_memory = nodes_sorted_by_used_memory_reverse[-1]
      print(node_less_used_memory)
      print('')

      print('---> Alocando o pod ' + pod_to_evict['name'] + ' em um node específico:')
      pod.schedule(node_less_used_memory['name'])
      print('')

    else: 

      print('---> Não há pod a ser despejado no node selecionado!')
      print('')

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
