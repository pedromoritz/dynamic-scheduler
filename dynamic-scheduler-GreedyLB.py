#!/usr/bin/env python3

import time
import k8s_helper_core as khc
from apscheduler.schedulers.background import BackgroundScheduler
import heapq

def get_round_robin_plan(pods, nodes):
  allocation_plan = {} 
  rr_counter = 0
  for pod in pods:
    allocation_plan[pod['name']] = nodes[rr_counter]['name']
    rr_counter = rr_counter + 1 if rr_counter < len(nodes) - 1 else 0
  return allocation_plan  

def get_greedylb_plan(chare_objects, processors, background_load):
  objHeap = list(map(lambda n: (n['usage']['memory'], n['name']), chare_objects))
  print(objHeap)
  heapq._heapify_max(objHeap)
  nodeHeap = list(map(lambda n: (background_load, n['name']), processors))
  print(nodeHeap)
  heapq.heapify(nodeHeap)
  allocation_plan = {}
  for i in objHeap:
    c = heapq._heappop_max(objHeap)
    donor = heapq.heappop(nodeHeap)
    allocation_plan[c[1]] = donor[1]
    new_donor = list(donor)
    new_donor[0] += c[0]
    print('---------')
    print('pod: ' + c[1])
    print('node: ' + new_donor[1])
    heapq.heappush(nodeHeap, tuple(new_donor))
  return allocation_plan

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

  not_ready_pods = cluster.not_ready_pods
  print('not_ready_pods')
  print(not_ready_pods)
  if len(not_ready_pods) > 0:
    return 

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

  if (percentual_delta > 10 or True):

    all_pods = []

    for node_item in nodes:
      node = khc.Node(node_item['name'])
      all_pods = all_pods + node.pods

    print('---> Criando uma lista de alocação')
#    allocation_plan = get_round_robin_plan(all_pods, nodes) 
    allocation_plan = get_greedylb_plan(all_pods, nodes, 1000000)

    for allocation_plan_item in allocation_plan:
      print('{' + allocation_plan_item + ': ' + allocation_plan[allocation_plan_item] + '}')

    cluster.set_allocation_plan(allocation_plan)

scheduling_workflow()
# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(scheduling_workflow, 'interval', seconds=30)
scheduler.start()
#timestamp;pod1;pod2;pod3;pod4;node1;node2
#000000000;  40;  40; 100;  20;1,2,3;4
# keeping script running
while True:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    scheduler.shutdown()
    break
