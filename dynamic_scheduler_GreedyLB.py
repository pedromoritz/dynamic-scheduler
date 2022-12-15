#!/usr/bin/env python3

import time
import k8s_scheduling_extension as kse
from apscheduler.schedulers.background import BackgroundScheduler
import heapq

def get_greedylb_plan(chare_objects, processors, background_load):
  print(chare_objects)
  print(processors)
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
  cluster = kse.Cluster()
  nodes = cluster.nodes
  if len(cluster.not_ready_pods) > 0:
    return 
#  print(cluster.info)
  pods = []
  for node_item in nodes:
    node = kse.Node(node_item['name'])
    pods = pods + node.pods
  allocation_plan = get_greedylb_plan(pods, nodes, 1000000)
  cluster.set_allocation_plan(allocation_plan)

#metrics_file = open('metrics_dynamic_scheduler_memory.csv', mode='w')
#metrics_file.write('timestamp,node1,node2,node3,pod1,pod2,pod3,pod4,pod5,pod6' + '\n')
#metrics_file.close()

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
