#!/usr/bin/env python3

import time
import k8s_helper_core as khc
from apscheduler.schedulers.background import BackgroundScheduler
from heapq import heappop, heappush, heapify

def get_round_robin_plan(pods, nodes):
  allocation_plan = {} 
  rr_counter = 0
  for pod in pods:
    allocation_plan[pod['name']] = nodes[rr_counter]['name']
    rr_counter = rr_counter + 1 if rr_counter < len(nodes) - 1 else 0
  return allocation_plan  

def get_greedylb_plan(chare_objects, processors, background_load):
  for pod in chare_objects:
    print(pod)

  transformed_chare_objects = map(lambda n: [n['usage']['memory'], n['name']], chare_objects) 

  heap = []
  heapify(heap)
  for pod in transformed_chare_objects:
    heappush(heap, pod)
print("The Head value of heap is : "+str(-1 * heap[0]))
print("Heap elements are : ")
for i in heap:
    print(-1 * i, end = ' ')
print("\n")
element = heappop(heap)



  for pod in transformed_chare_objects:
    print(pod)

  allocation_plan = {}
  return allocation_plan
#itens_na_mochila = []
#peso_da_mochila = 0
# ordenando a lista pela razão valor/peso do item
#itens_ordenados = sorted(itens, key=lambda item: item[0]/item[1], reverse=True)
# executando o algoritmo guloso
#for item_ordenado in itens_ordenados:
#peso_item_ordenado = item_ordenado[1]
#if peso_item_ordenado + peso_da_mochila <= capacidade_mochila:
#itens_na_mochila.append(item_ordenado)
#peso_da_mochila += peso_item_ordenado
#return itens_na_mochila
# lista de items [valor, peso]
#itens = [
#[140, 10],
#[120, 6],
#[100, 2],
#[80, 5],
#[90, 5]
#]
# capacidade máxima de peso da mochila
#capacidade_mochila = 13
#itens_colocados_na_mochila = problema_da_mochila(itens, capacidade_mochila)
#print(itens_colocados_na_mochila)


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

  print('---> Verificando se a diferença entre os nodes selecionados é maior que 20% da capacidade máxima:')
  absolute_delta = (node_more_used_memory['usage']['memory'] - node_less_used_memory['usage']['memory'])
  percentual_delta = round((absolute_delta / node_more_used_memory['capacity']['memory']) * 100, 2)
  print('absolute delta: ' + str(absolute_delta) + 'KB | ' + 'percentual delta: ' + str(percentual_delta) + '%', end="\n\n")

  if (percentual_delta > 20 or True):

    all_pods = []

    for node_item in nodes:
      node = khc.Node(node_item['name'])
      all_pods = all_pods + node.pods

    print('---> Criando uma lista de alocação')
#    allocation_plan = get_round_robin_plan(all_pods, nodes) 
    allocation_plan = get_greedylb_plan(all_pods, nodes, 1000)

    for allocation_plan_item in allocation_plan:
      print(allocation_plan_item)

#    cluster.set_allocation_plan(allocation_plan)

scheduling_workflow()
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
