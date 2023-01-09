#!/usr/bin/env python3

import time
import kse as kse
from apscheduler.schedulers.background import BackgroundScheduler
import heapq

CSV_FILENAME = 'metrics_dynamic_scheduler_GreedyLB_memory.csv'
INTERVAL = 10

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
  return dict(sorted(allocation_plan.items()))

# workflow definitions
def scheduling_workflow():
  print('scheduling_workflow...')
  cluster = kse.Cluster()
  kse.Utils.write_file(CSV_FILENAME, ','.join(map(str, cluster.get_info()['data'])))
  nodes = cluster.get_nodes()
  if len(cluster.get_unready_pods()) > 0:
    return 
  pods = []
  for node_item in nodes:
    this_node_pods = cluster.get_pods_from_node(node_item['name'])
    pods = pods + this_node_pods
  allocation_plan = get_greedylb_plan(pods, nodes, 1000000)
  cluster.set_allocation_plan(allocation_plan)

cluster = kse.Cluster()
#info = cluster.get_info()
kse.Utils.write_file(CSV_FILENAME, ','.join(map(str, cluster.get_info()['header'])), 'w')

scheduling_workflow()
# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(scheduling_workflow, 'interval', seconds=INTERVAL)
scheduler.start()

# keeping script running
while True:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    scheduler.shutdown()
    break
