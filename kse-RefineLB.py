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
  print('chare_objects')
  print(chare_objects)
  print('')
  print('processors')
  print(processors)
  print('')
  cluster = kse.Cluster()
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
      print('heavy')
      print(processor)
      heavyProcs.append(processor)
    else:
      print('light')
      print(processor)
      lightProcs.append(processor)
  print('heavyProcs before heapify')
  print(heavyProcs)
  heavyProcsMapped = list(map(lambda n: (n['usage']['memory'], n['name']), heavyProcs))
  heapq._heapify_max(heavyProcsMapped)
  print('heavyProcsMapped')
  print(heavyProcsMapped)
  print('')
  print('lightProcs')
  print(lightProcs)
  print('')
  finalProcs = []
  while len(heavyProcs) > 0:
    print('starting 1st while')
    donor = heapq._heappop_max(heavyProcs)
    print('donor')
    print(donor) 
    print('')
    while len(lightProcs) > 0:
      print('starting 2nd while')
      lightProc = lightProcs.pop()
      print('ligthProc choosen')
      print(lightProc)
      print('')
      pods_from_donor = cluster.get_pods_from_node(donor['name'])
      print('pods from donor')
      print(pods_from_donor)
      pods_from_donor_sorted = list(map(lambda n: (n['usage']['memory'], n['name']), pods_from_donor))
      donor_best_pod = pods_from_donor_sorted[-1]
      print('donor_best_pod')
      print(donor_best_pod)
      if donor_best_pod[0] + lightProc['usage']['memory'] < procs_memory_average:
        print('break')
        break
    #deAssign(obj, donor)
    #assign(obj, lightProc)
    allocation_plan[donor_best_pod[1]] = donor['name']
  return dict(sorted(allocation_plan.items()))

# workflow definitions
def scheduling_workflow():
  global COUNTER
  global INTERVAL
  global CSV_FILENAME 
  print('scheduling_workflow...')
  cluster = kse.Cluster()
  #cluster.do_info_snapshot(CSV_FILENAME, COUNTER)
  #COUNTER += INTERVAL
  nodes = cluster.get_nodes()
  #if len(cluster.get_unready_pods()) > 0:
  #  return 
  pods = []
  for node_item in nodes:
    this_node_pods = cluster.get_pods_from_node(node_item['name'])
    pods = pods + this_node_pods
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
