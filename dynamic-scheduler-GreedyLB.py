#!/usr/bin/env python3

import time
import k8s_helper_core as khc
from apscheduler.schedulers.background import BackgroundScheduler
import heapq
import csv

metrics_file = open('metrics.csv', mode='w')
field_names = ['timestamp', 'node1', 'node2', 'node3', 'pod1', 'pod2', 'pod3', 'pod4', 'pod5', 'pod6']
metrics_writer = csv.writer(metrics_file)
metrics_writer.writerow(field_names)
print(123)

def get_round_robin_plan(pods, nodes):
  allocation_plan = {} 
  rr_counter = 0
  for pod in pods:
    allocation_plan[pod['name']] = nodes[rr_counter]['name']
    rr_counter = rr_counter + 1 if rr_counter < len(nodes) - 1 else 0
  return allocation_plan  

def get_greedylb_plan(chare_objects, processors, background_load):
  objHeap = list(map(lambda n: (n['usage']['memory'], n['name']), chare_objects))
  heapq._heapify_max(objHeap)
  nodeHeap = list(map(lambda n: (background_load, n['name']), processors))
  heapq.heapify(nodeHeap)
  allocation_plan = {}
  objHeapSize = len(objHeap)
  for i in range(objHeapSize):
    c = heapq._heappop_max(objHeap)
    donor = heapq.heappop(nodeHeap)
    allocation_plan[c[1]] = donor[1]
    new_donor = list(donor)
    new_donor[0] += c[0]
    heapq.heappush(nodeHeap, tuple(new_donor))
  allocation_plan = dict(sorted(allocation_plan.items()))
  return allocation_plan

# workflow definitions
def scheduling_workflow():
  print('##########################################')
  print('Iniciando workflow', end="\n\n")
  cluster = khc.Cluster()
  nodes = cluster.nodes

  if len(cluster.not_ready_pods) > 0:
    return 
  pods = []
  current_allocation = {}
  for node_item in nodes:
    node = khc.Node(node_item['name'])
    pods = pods + node.pods
    for pods_item in node.pods:
      current_allocation[pods_item['name']] = node_item['name']
  current_allocation = dict(sorted(current_allocation.items())) 

#timestamp;pod1;pod2;pod3;pod4;node1;node2
#000000000;  40;  40; 100;  20;1,2,3;4A
  csv_record = str(time.time()) + ',' \
    + str(nodes[0]['usage']['memory']) + ',' \
    + str(nodes[1]['usage']['memory']) + ',' \
    + str(nodes[2]['usage']['memory']) + ',' \
    + str(pods[0]['usage']['memory']) + ',' \
    + str(pods[1]['usage']['memory']) + ',' \
    + str(pods[2]['usage']['memory']) + ',' \
    + str(pods[3]['usage']['memory']) + ',' \
    + str(pods[4]['usage']['memory']) + ',' \
    + str(pods[5]['usage']['memory'])
  metrics_writer.writerow(csv_record)

  print('---> Current allocation:')
  for item in current_allocation:
    print('{' + item + ': ' + current_allocation[item] + '}')

  print('---> New allocation:')
  allocation_plan = get_greedylb_plan(pods, nodes, 1000000)
  for item in allocation_plan:
    print('{' + item + ': ' + allocation_plan[item] + '}')

  cluster.set_allocation_plan(allocation_plan)

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
