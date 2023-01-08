#!/usr/bin/env python3

import time
import kse as kse
from apscheduler.schedulers.background import BackgroundScheduler
import heapq

CSV_FILENAME = 'metrics_dynamic_scheduler_RefineLB_memory.csv'

def get_refinelb_plan(chare_objects, processors):
  allocation_plan = {}
  heavyProcs = []
  lightProcs = []
  # calculating threshold
  procs_memory_values = list(map(lambda n: n['usage']['memory'], processors))
  procs_memory_average = round(reduce(lambda x, y: x + y, procs_memory_values) / len(procs_memory_values), 0) 
  margin = 1.0 # >= 1.0
  threshold = procs_memory_average * margin
  print(threshold)
  # defining heavyProcs and lightProcs based on threshold
  for processor in processors:
    if int(processor['usage']['memory']) > threshold:
      heavyProcs.append(processor)
    else:
      lightProcs.append(processor)
  heapq._heapify_max(heavyProcs)
  print(heavyProcs)
  print(lightProcs)
  while len(heavyProcs) > 0:
    print('iteracao a')
    donor = heapq._heappop_max(heavyProcs)
    print(donor) 
#    while len(lightProcs) > 0:
    print('iteracao b')
    node = kse.Node(donor['name'])
    print(node.pods)
  return dict(sorted(allocation_plan.items()))

# workflow definitions
def scheduling_workflow():
  print('scheduling_workflow...')
  cluster = kse.Cluster()
  nodes = cluster.get_nodes()
  if len(cluster.get_unready_pods()) > 0:
    return 
  info = cluster.get_info() 
  kse.Utils.write_file(CSV_FILENAME, ','.join(map(str, info['data'])))
  pods = []
  for node_item in nodes:
    this_node_pods = cluster.get_pods_from_node(node_item['name'])
    pods = pods + this_node_pods
  allocation_plan = get_refinelb_plan(pods, nodes)
  cluster.set_allocation_plan(allocation_plan)

cluster = kse.Cluster()
info = cluster.get_info()
kse.Utils.write_file(CSV_FILENAME, ','.join(map(str, info['header'])), 'w')

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
