#!/usr/bin/env python3

import time
import kse as kse
from apscheduler.schedulers.background import BackgroundScheduler
import heapq
import sys
from functools import reduce

CSV_FILENAME_BASE = sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'_'+sys.argv[4]+'_'+sys.argv[5]+'_'+sys.argv[6]+'.csv'
INTERVAL = 60
COUNTER = -2
METRIC = sys.argv[6]
MARGIN = 1.05

def get_refinelb_plan(processors):
  global MARGIN
  allocation_plan = {}
  heavyProcs = []
  lightProcs = []
  # calculating threshold
  procs_values = list(map(lambda n: n['usage'][METRIC], processors))
  procs_average = round(reduce(lambda x, y: x + y, procs_values) / len(procs_values), 0)
  print('procs_average')
  print(procs_average)
  threshold = procs_average * MARGIN
  # defining heavyProcs and lightProcs based on threshold
  for processor in processors:
    if int(processor['usage'][METRIC]) < procs_average:
      print('light')
      print(processor)
      print('')
      lightProcs.append(processor)
    else:
      print('heavy')
      print(processor)
      print('')
      heavyProcs.append(processor)
  heavyProcs.sort(key=lambda x: x['usage'][METRIC])
  lightProcs.sort(key=lambda x: x['usage'][METRIC])
  finalProcs = []

  while len(heavyProcs) > 0:
    print('--------------------')
    print('itera heavyProcs')
    print('')
    donor = heavyProcs.pop()
    print('donor')
    print(donor)
    print('')
    for index, lightProc in enumerate(lightProcs):
      print('--------------------')
      print('itera lightProcs')
      pods_from_donor = donor['pods']
      pods_from_donor_sorted = sorted(list(map(lambda n: (n['usage'][METRIC], n['name']), pods_from_donor)), reverse=True)
      donor_best_pod = pods_from_donor_sorted[0]
      print('donor_best_pod')
      print(donor_best_pod[1])
      print(donor_best_pod[0])
      print('')
      print('lightProc[usage][METRIC]')
      print(lightProc['usage'][METRIC])
      print('')
      print('donor_best_pod[0] + lightProc[usage][METRIC]')
      print(donor_best_pod[0] + lightProc['usage'][METRIC])
      print('procs_average')
      print(procs_average)
      if donor_best_pod[0] + lightProc['usage'][METRIC] > threshold:
        print('continue')
        continue
      else:
        print('------> pod choosed')
        print(lightProcs[index]['usage'][METRIC])
        # deassign best pod from donor
        donor['pods'] = [d for d in donor['pods'] if d['name'] != donor_best_pod[1]]
        # reassign best pod
        lightProcs[index]['usage'][METRIC] = lightProcs[index]['usage'][METRIC] + donor_best_pod[0]
        allocation_plan[donor_best_pod[1]] = lightProc['name']
        #break
  return dict(sorted(allocation_plan.items()))

# workflow definitions
def scheduling_workflow():
  global COUNTER
  global INTERVAL
  global CSV_FILENAME_BASE 
  cluster = kse.Cluster()
  if COUNTER == -2:
    COUNTER = -1
  else:
    COUNTER = 0 if COUNTER == -1 else COUNTER + INTERVAL
    nodes = cluster.get_nodes()
    cluster.do_info_snapshot('metrics_'+CSV_FILENAME_BASE, COUNTER, nodes)
  if len(cluster.get_unready_pods()) > 0:
    return 
  if COUNTER > 0:
    allocation_plan = get_refinelb_plan(nodes)
    cluster.set_allocation_plan(allocation_plan, 'migrations_'+CSV_FILENAME_BASE, COUNTER)

scheduling_workflow()
# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(scheduling_workflow, 'interval', seconds=INTERVAL)
scheduler.start()

# keeping script running
while COUNTER < 600:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    scheduler.shutdown()
    break
