#!/usr/bin/env python3

import time
import kse as kse
from apscheduler.schedulers.background import BackgroundScheduler
import heapq
import sys

CSV_FILENAME_BASE = sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'_'+sys.argv[4]+'_'+sys.argv[5]+'_'+sys.argv[6]+'.csv'
INTERVAL = 60
COUNTER = 0
METRIC = sys.argv[6]

def get_greedylb_plan(chare_objects, processors, background_load):
  objHeap = list(map(lambda n: (n['usage'][METRIC], n['name']), chare_objects))
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
  global COUNTER
  global INTERVAL
  global CSV_FILENAME_BASE 
  print('scheduling_workflow...')
  cluster = kse.Cluster()
  cluster.do_info_snapshot('metrics_'+CSV_FILENAME_BASE, COUNTER)
  nodes = cluster.get_nodes()
  if len(cluster.get_unready_pods()) > 0:
    return 
  pods = []
  for node_item in nodes:
    this_node_pods = cluster.get_pods_from_node(node_item['name'])
    pods = pods + this_node_pods
  if COUNTER > 0:
    allocation_plan = get_greedylb_plan(pods, nodes, 1000000)
    cluster.set_allocation_plan(allocation_plan, 'migrations_'+CSV_FILENAME_BASE, COUNTER)
  COUNTER += INTERVAL

scheduling_workflow()
# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(scheduling_workflow, 'interval', seconds=INTERVAL)
scheduler.start()

# keeping script running
while COUNTER <= 1800:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    scheduler.shutdown()
    break
