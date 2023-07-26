#!/usr/bin/env python3

import time
import kse as kse
from apscheduler.schedulers.background import BackgroundScheduler
import heapq
import sys
from functools import reduce

CSV_FILENAME_BASE = sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'_'+sys.argv[4]+'_'+sys.argv[5]+'_'+sys.argv[6]+'.csv'
INTERVAL = 60
COUNTER = 0
METRIC = sys.argv[6]

def get_refinelb_plan(processors):
  allocation_plan = {}
  heavyProcs = []
  lightProcs = []
  # calculating threshold
  procs_values = list(map(lambda n: n['usage'][METRIC], processors))
  procs_average = round(reduce(lambda x, y: x + y, procs_values) / len(procs_values), 0)
  print('procs_average')
  print(procs_average)
  margin = 1.05
  threshold = procs_average * margin
  # defining heavyProcs and lightProcs based on threshold
  for processor in processors:
    if int(processor['usage'][METRIC]) < threshold:
      lightProcs.append(processor)
    else:
      heavyProcs.append(processor)
  heavyProcs.sort(key=lambda x: x['usage'][METRIC])
  lightProcs.sort(key=lambda x: x['usage'][METRIC])
  finalProcs = []
  print(lightProcs)
  print(heavyProcs)
  print('')

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
      if donor_best_pod[0] + lightProc['usage'][METRIC] > threshold:
        print('continue')
        continue
      else:
        print('------> pod choosed')
        print(lightProcs[index]['usage']['memory'])
        # deassign best pod from donor
        donor['pods'] = [d for d in donor['pods'] if d['name'] != donor_best_pod[1]]
        # reassign best pod
        lightProcs[index]['usage']['memory'] = lightProcs[index]['usage']['memory'] + donor_best_pod[0]
        allocation_plan[donor_best_pod[1]] = lightProc['name']
        break
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
  if COUNTER > 0:
    allocation_plan = get_refinelb_plan(nodes)
    cluster.set_allocation_plan(allocation_plan, 'migrations_'+CSV_FILENAME_BASE, COUNTER)
  COUNTER += INTERVAL

scheduling_workflow()
# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(scheduling_workflow, 'interval', seconds=INTERVAL)
scheduler.start()

# keeping script running
while COUNTER <= 600:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    scheduler.shutdown()
    break
