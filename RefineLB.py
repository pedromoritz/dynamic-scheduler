#!/usr/bin/env python3

import time
import kse as kse
from apscheduler.schedulers.background import BackgroundScheduler
import sys
from functools import reduce

CSV_FILENAME_BASE = sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'_'+sys.argv[4]+'_'+sys.argv[5]+'_'+sys.argv[6]+'.csv'
INTERVAL = 60
COUNTER = -2
METRIC = sys.argv[6]

def get_refinelb_plan(nodes):
  allocationPlan = {}
  overLoad = 1.05
  heavyNodes = []
  lightNodes = []
  # calculating averageLoad
  nodesValues = list(map(lambda n: n['usage'][METRIC], nodes))
  averageLoad = round(reduce(lambda x, y: x + y, nodesValues) / len(nodesValues), 0)
  # defining heavyNodes and lightNodes based on threshold
  for node in nodes:
    if node['usage'][METRIC] > overLoad * averageLoad:
      heavyNodes.append(node)
    if node['usage'][METRIC] < averageLoad:
      lightNodes.append(node)
  heavyNodes.sort(key=lambda x: x['usage'][METRIC])

  print('heavyNodes')
  print(heavyNodes)
  print('')

  print('lightNodes')
  print(lightNodes)
  print('')

  done = True
  while done:
    if len(heavyNodes) > 0:
      donor = heavyNodes.pop()
    else:
      break

    highestLoadFromDonor = 0
    bestPodFromDonor = None
    bestNodeFromLightNodes = None

    for indexlightNode, currentLightNode in enumerate(lightNodes):
      for indexPodFromDonor, currentPodFromDonor in enumerate(donor['pods']):
        #print(currentPodFromDonor)
        if currentPodFromDonor['usage'][METRIC] + currentLightNode['usage'][METRIC] < overLoad * averageLoad:
          if currentPodFromDonor['usage'][METRIC] > highestLoadFromDonor:
            highestLoadFromDonor = currentPodFromDonor['usage'][METRIC]
            bestPodFromDonor = currentPodFromDonor
            bestNodeFromLightNodes = currentLightNode

    if bestPodFromDonor is not None:
      # deassign
      donorIndexAtNodes = nodes.index(next(filter(lambda n: n.get('name') == donor['name'], nodes)))
      nodes[donorIndexAtNodes]['pods'] = [d for d in donor['pods'] if d['name'] != bestPodFromDonor['name']]
      nodes[donorIndexAtNodes]['usage'][METRIC] -= bestPodFromDonor['usage'][METRIC]
      # assign
      bestNodeIndexAtNodes = nodes.index(next(filter(lambda n: n.get('name') == bestNodeFromLightNodes['name'], nodes)))
      nodes[bestNodeIndexAtNodes]['pods'].append(bestPodFromDonor)
      nodes[bestNodeIndexAtNodes]['usage'][METRIC] += bestPodFromDonor['usage'][METRIC]
    else:
      break

    print('lightNodes antes')
    print(lightNodes)
    print('')

    print("bestNodeFromLightNodes['usage'][METRIC]")
    print(bestNodeFromLightNodes['usage'][METRIC])
    print('')

    print('averageLoad')
    print(averageLoad)
    print('')

    if bestNodeFromLightNodes['usage'][METRIC] > averageLoad:
      lightNodes = [d for d in lightNodes if d['name'] != bestNodeFromLightNodes['name']]

    print('lightNodes depois')
    print(lightNodes)
    print('')

    if donor['usage'][METRIC] > overLoad * averageLoad:
      heavyNodes.append(donor)
      heavyNodes.sort(key=lambda x: x['usage'][METRIC])      
    elif donor['usage'][METRIC] < averageLoad:
      lightNodes.append(donor)

  for node in nodes:
    for pod in node['pods']:
      allocationPlan[pod['name']] = node['name']

  return dict(sorted(allocationPlan.items()))

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
