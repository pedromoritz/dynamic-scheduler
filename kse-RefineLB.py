#!/usr/bin/env python3

import time
import kse as kse
from apscheduler.schedulers.background import BackgroundScheduler
import heapq
import sys
from functools import reduce

CSV_FILENAME_BASE = sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'.csv'
INTERVAL = 60
COUNTER = 0

def get_refinelb_plan(processors):
  allocation_plan = {}
  heavyProcs = []
  lightProcs = []
  # calculating threshold
  procs_memory_values = list(map(lambda n: n['usage']['memory'], processors))
  procs_memory_average = round(reduce(lambda x, y: x + y, procs_memory_values) / len(procs_memory_values), 0) 
  margin = 1.002 # >= 1.002
  threshold = procs_memory_average * margin
  # defining heavyProcs and lightProcs based on threshold
  for processor in processors:
    if int(processor['usage']['memory']) > threshold:
      heavyProcs.append(processor)
    else:
      lightProcs.append(processor)
  heavyProcsMapped = list(map(lambda n: (n['usage']['memory'], n['name']), heavyProcs))
  heapq._heapify_max(heavyProcsMapped)
  finalProcs = []
  while len(heavyProcs) > 0:
    donor = heapq._heappop_max(heavyProcs)
    while len(lightProcs) > 0:
      lightProc = lightProcs.pop()
      pods_from_donor = donor['pods']
      pods_from_donor_sorted = list(map(lambda n: (n['usage']['memory'], n['name']), pods_from_donor))
      donor_best_pod = pods_from_donor_sorted[-1]
      if donor_best_pod[0] + lightProc['usage']['memory'] < procs_memory_average:
        break
    donor['pods'] = [d for d in donor['pods'] if d['name'] != donor_best_pod[1]]
    finalProcs.append(donor)
    lightProcPods = lightProc['pods']
    lightProcPods.append({'name': donor_best_pod[1]})
    lightProc['pods'] = lightProcPods
    finalProcs.append(lightProc)
  for node in finalProcs:
    for pod in node['pods']:
      allocation_plan[pod['name']] = node['name'] 
  return dict(sorted(allocation_plan.items()))

# workflow definitions
def scheduling_workflow():
  global COUNTER
  global INTERVAL
  global CSV_FILENAME_BASE 
  print('scheduling_workflow...')
  cluster = kse.Cluster()
  cluster.do_info_snapshot('metrics_'+CSV_FILENAME_BASE, COUNTER)
  COUNTER += INTERVAL
  if len(cluster.get_unready_pods()) > 0:
    return 

  #nodes = [{'name': 'ppgcc-m02', 'pods': [{'name': 'pod-1-9dc86b49d-snz6k', 'usage': {'memory': 129256, 'cpu': 47474876}}, {'name': 'pod-4-7b699966b7-ngd44', 'usage': {'memory': 88452, 'cpu': 80833568}}], 'type': 'worker', 'capacity': {'memory': 4012876, 'cpu': 2000000000}, 'usage': {'memory': 1038372, 'cpu': 203905727}}, {'name': 'ppgcc-m03', 'pods': [{'name': 'pod-2-595595f665-v9lx7', 'usage': {'memory': 119068, 'cpu': 50038718}}, {'name': 'pod-5-c45cfd9f4-cj5r8', 'usage': {'memory': 93560, 'cpu': 101884462}}], 'type': 'worker', 'capacity': {'memory': 4012876, 'cpu': 2000000000}, 'usage': {'memory': 984432, 'cpu': 168151939}}, {'name': 'ppgcc-m04', 'pods': [{'name': 'pod-3-6c8575488-xrg6b', 'usage': {'memory': 142528, 'cpu': 83090882}}, {'name': 'pod-6-5d9f974c89-7fmps', 'usage': {'memory': 68348, 'cpu': 45351798}}], 'type': 'worker', 'capacity': {'memory': 4012876, 'cpu': 2000000000}, 'usage': {'memory': 983928, 'cpu': 172164950}}]

  allocation_plan = get_refinelb_plan(nodes)
  print(allocation_plan)
  cluster.set_allocation_plan(allocation_plan, 'migrations_'+CSV_FILENAME_BASE, COUNTER)

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
