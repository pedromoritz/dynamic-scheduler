#!/usr/bin/env python3

import time
import kse as kse
from apscheduler.schedulers.background import BackgroundScheduler
import heapq
from functools import reduce

def get_refinelb_plan(processors):
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

#  objHeap = list(map(lambda n: (n['usage']['memory'], n['name']), chare_objects))
#  heapq._heapify_max(objHeap)
#  nodeHeap = list(map(lambda n: (background_load, n['name']), processors))
#  heapq.heapify(nodeHeap)
#  allocation_plan = {}
#  objHeapSize = len(objHeap)
#  for i in range(objHeapSize):
#    c = heapq._heappop_max(objHeap)
#    donor = heapq.heappop(nodeHeap)
#    allocation_plan[c[1]] = donor[1]
#    new_donor = list(donor)
#    new_donor[0] += c[0]
#    heapq.heappush(nodeHeap, tuple(new_donor))
  return dict(sorted(allocation_plan.items()))

processors = [{'name': 'ppgcc-m02', 'type': 'worker', 'capacity': {'memory': 4012876, 'cpu': 2000000000}, 'usage': {'memory': 1980396, 'cpu': 1119789161}, 'pods': [{'name': 'pod-1-858599d969-rm9dk', 'usage': {'memory': 1045672, 'cpu': 1095626655}}, {'name': 'pod-4-6f77646f66-kt4q6', 'usage': {'memory': 45768, 'cpu': 5503}}]},	{'name': 'ppgcc-m03', 'type': 'worker', 'capacity': {'memory': 4012876, 'cpu': 2000000000}, 'usage': {'memory': 2025424, 'cpu': 972677352}, 'pods': [{'name': 'pod-3-77d6d49bb7-f4bqj', 'usage': {'memory': 1283696, 'cpu': 1103796284}}, {'name': 'pod-5-678bc6fd77-k9qp2', 'usage': {'memory': 44472, 'cpu': 6495}}]}, {'name': 'ppgcc-m04', 'type': 'worker', 'capacity': {'memory': 4012876, 'cpu': 2000000000}, 'usage': {'memory': 2147112, 'cpu': 977669603}, 'pods': [{'name': 'pod-2-6dcc4fc5bd-x7phd', 'usage': {'memory': 894916, 'cpu': 1052973996}}, {'name': 'pod-6-675c8855d4-m6ln5', 'usage': {'memory': 45892, 'cpu': 5283}}]}]

result = get_refinelb_plan(processors)
print(result)

# workflow definitions
def scheduling_workflow():
  cluster = kse.Cluster()
  nodes = cluster.nodes
  if len(cluster.not_ready_pods) > 0:
    return 
  print(cluster.info)
  pods = []
  for node_item in nodes:
    node = kse.Node(node_item['name'])
    pods = pods + node.pods
  allocation_plan = get_refinelb_plan(pods, nodes, 1000000)
  cluster.set_allocation_plan(allocation_plan)

#metrics_file = open('metrics_dynamic_scheduler_memory.csv', mode='w')
#metrics_file.write('timestamp,node1,node2,node3,pod1,pod2,pod3,pod4,pod5,pod6' + '\n')
#metrics_file.close()

#scheduling_workflow()
# creating a timer for workflow trigger
#scheduler = BackgroundScheduler()
#scheduler.add_job(scheduling_workflow, 'interval', seconds=60)
#scheduler.start()

# keeping script running
#while True:
#  try:
#    time.sleep(0.1)
#  except KeyboardInterrupt:
#    scheduler.shutdown()
#    break
