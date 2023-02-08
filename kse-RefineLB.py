#!/usr/bin/env python3

import time
import kse as kse
from apscheduler.schedulers.background import BackgroundScheduler
import heapq
import sys
from functools import reduce

CSV_FILENAME = 'metrics_'+sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'.csv'
INTERVAL = 60
COUNTER = 0

def get_refinelb_plan(chare_objects, processors):
  allocation_plan = {}
  heavyProcs = []
  lightProcs = []
  # calculating threshold
  procs_memory_values = list(map(lambda n: n['usage']['memory'], processors))
  procs_memory_average = round(reduce(lambda x, y: x + y, procs_memory_values) / len(procs_memory_values), 0) 
  margin = 1.002 # >= 1.002
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
    donor = heapq._heappop_max(heavyProcs)
    print(donor) 
    while (lightProc = lightProcs.next()) do
      obj, lightProc = getBestProcAndObj(donor, Vo)
      if (obj.load+lightProc.load < avgLoad) break
    deAssign(obj, donor)
    assign(obj, lightProc)
  return dict(sorted(allocation_plan.items()))

# workflow definitions
def scheduling_workflow():
  global COUNTER
  global INTERVAL
  global CSV_FILENAME 
  print('scheduling_workflow...')
  cluster = kse.Cluster()
  cluster.do_info_snapshot(CSV_FILENAME, COUNTER)
  COUNTER += INTERVAL
#  nodes = cluster.get_nodes()
#  if len(cluster.get_unready_pods()) > 0:
#    return 
#  pods = []
#  for node_item in nodes:
#    this_node_pods = cluster.get_pods_from_node(node_item['name'])
#    pods = pods + this_node_pods

  pods = [{'name': 'pod-1-59d4499f-ffshf', 'usage': {'memory': 41916, 'cpu': 48078169}}, {'name': 'pod-4-84f645cdb4-gk2r9', 'usage': {'memory': 41792, 'cpu': 31765}}, {'name': 'pod-7-8647bdf857-s6m4h', 'usage': {'memory': 41708, 'cpu': 57752727}}, {'name': 'pod-8-5d7c64cb76-8xdn8', 'usage': {'memory': 41084, 'cpu': 64102808}}, {'name': 'pod-10-6f87c978df-8hcx5', 'usage': {'memory': 43060, 'cpu': 10236}}, {'name': 'pod-11-8447866574-4j2cd', 'usage': {'memory': 41312, 'cpu': 56116631}}, {'name': 'pod-2-78495b5d46-5vh27', 'usage': {'memory': 41704, 'cpu': 32291}}, {'name': 'pod-3-6d78c94cf7-vm855', 'usage': {'memory': 41316, 'cpu': 51804634}}, {'name': 'pod-12-7566ccbd99-k4p54', 'usage': {'memory': 41396, 'cpu': 51220528}}, {'name': 'pod-5-6889667dbc-c64bp', 'usage': {'memory': 41604, 'cpu': 59010639}}, {'name': 'pod-6-9f9fbcd58-fhczt', 'usage': {'memory': 42104, 'cpu': 64759918}}, {'name': 'pod-9-8c8f4bbcf-mzh68', 'usage': {'memory': 50140, 'cpu': 66642779}}]

  nodes = [{'name': 'ppgcc-m02', 'type': 'worker', 'capacity': {'memory': 4012876, 'cpu': 2000000000}, 'usage': {'memory': 1155600, 'cpu': 270956631}}, {'name': 'ppgcc-m03', 'type': 'worker', 'capacity': {'memory': 4012876, 'cpu': 2000000000}, 'usage': {'memory': 1187416, 'cpu': 349423548}}, {'name': 'ppgcc-m04', 'type': 'worker', 'capacity': {'memory': 4012892, 'cpu': 2000000000}, 'usage': {'memory': 1166812, 'cpu': 315672081}}]

  allocation_plan = get_refinelb_plan(pods, nodes)
  print(allocation_plan)
  cluster.set_allocation_plan(allocation_plan)

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
