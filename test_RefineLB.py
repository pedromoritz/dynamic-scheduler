#!/usr/bin/env python3

import heapq
from functools import reduce

METRIC = 'memory'

def get_refinelb_plan(processors):
  allocation_plan = {}
  heavyProcs = []
  lightProcs = []
  # calculating threshold
  procs_values = list(map(lambda n: n['usage'][METRIC], processors))
  procs_average = round(reduce(lambda x, y: x + y, procs_values) / len(procs_values), 0) 
  margin = 1.003 # >= 1.003
  threshold = procs_average * margin
  # defining heavyProcs and lightProcs based on threshold
  for processor in processors:
    if int(processor['usage'][METRIC]) < threshold:
      lightProcs.append(processor)
    else:
      heavyProcs.append(processor)
  heavyProcsMapped = list(map(lambda n: (n['usage'][METRIC], n['name']), heavyProcs))
  heapq._heapify_max(heavyProcsMapped)
  finalProcs = []
  while len(heavyProcs) > 0:
    donor = heapq._heappop_max(heavyProcs)
    #print('donor')
    #print(donor)
    #print('')
    for lightProc in lightProcs:
      #print('lightProc')
      #print(lightProc)
      #print('')
      pods_from_donor = donor['pods']
      pods_from_donor_sorted = sorted(list(map(lambda n: (n['usage'][METRIC], n['name']), pods_from_donor)), reverse=True)
      #print(pods_from_donor_sorted)
      donor_best_pod = pods_from_donor_sorted[0]
      #print(donor_best_pod)
      #print('')
      #print(donor_best_pod[0] + lightProc['usage'][METRIC])
      #print(procs_average)
      if donor_best_pod[0] + lightProc['usage'][METRIC] > procs_average:
        continue
      # deassign best pod from donor
      #print('deassign')
      donor['pods'] = [d for d in donor['pods'] if d['name'] != donor_best_pod[1]]
      #print('lightProc-->')
      #print(lightProc)
      lightProc['pods'].append({'name': donor_best_pod[1], 'usage': {'memory': donor_best_pod[0]}})
      #print(lightProc)
      finalProcs.append(lightProc)
  for node in finalProcs:
    for pod in node['pods']:
      allocation_plan[pod['name']] = node['name'] 
  return dict(sorted(allocation_plan.items()))

nodes = [{'name': 'ppgcc-m02', 'pods': [{'name': 'pod-10-8988d5d54-vl9vb', 'usage': {'memory': 182948, 'cpu': 261517052}}, {'name': 'pod-14-f9b476cbb-knkd6', 'usage': {'memory': 125304, 'cpu': 144685427}}, {'name': 'pod-18-57d947497d-6k28x', 'usage': {'memory': 46324, 'cpu': 27336030}}, {'name': 'pod-5-8cfcc8d96-ts64t', 'usage': {'memory': 80108, 'cpu': 67733927}}, {'name': 'pod-6-7c58786f49-p6m9r', 'usage': {'memory': 84280, 'cpu': 82387139}}], 'type': 'worker', 'capacity': {'memory': 2165980, 'cpu': 2000000000}, 'usage': {'memory': 1483700, 'cpu': 673951385}}, {'name': 'ppgcc-m03', 'pods': [{'name': 'pod-11-7b77bdc5df-gzzd9', 'usage': {'memory': 185996, 'cpu': 253664252}}, {'name': 'pod-16-686cc7846d-cvbx4', 'usage': {'memory': 66916, 'cpu': 60344454}}, {'name': 'pod-2-5f77b59d65-vkksh', 'usage': {'memory': 32040, 'cpu': 12062634}}, {'name': 'pod-3-546cdf5494-gdsb2', 'usage': {'memory': 24416, 'cpu': 11069103}}, {'name': 'pod-9-74976d75d8-s2qpp', 'usage': {'memory': 141016, 'cpu': 174283492}}], 'type': 'worker', 'capacity': {'memory': 2165984, 'cpu': 2000000000}, 'usage': {'memory': 1487328, 'cpu': 744656750}}, {'name': 'ppgcc-m04', 'pods': [{'name': 'pod-1-5d9b45689b-4kvgn', 'usage': {'memory': 11180, 'cpu': 2071848}}, {'name': 'pod-13-85b68c7f9-sspwk', 'usage': {'memory': 172052, 'cpu': 197030782}}, {'name': 'pod-17-545fdc5dc5-xk765', 'usage': {'memory': 55588, 'cpu': 46091700}}, {'name': 'pod-4-78898d8c5-hmvtg', 'usage': {'memory': 62164, 'cpu': 57940784}}, {'name': 'pod-7-5fb75f4dc4-g84wd', 'usage': {'memory': 142700, 'cpu': 192934705}}], 'type': 'worker', 'capacity': {'memory': 2165984, 'cpu': 2000000000}, 'usage': {'memory': 1384020, 'cpu': 626760463}}, {'name': 'ppgcc-m05', 'pods': [{'name': 'pod-12-74b4cb76d4-zbncd', 'usage': {'memory': 1000000, 'cpu': 247825232}}, {'name': 'pod-15-77b7cccb77-7zsq7', 'usage': {'memory': 1047320, 'cpu': 124036823}}, {'name': 'pod-19-56744df5fc-9qms4', 'usage': {'memory': 21828000, 'cpu': 9234117}}, {'name': 'pod-20-59fbf9f7-q8z77', 'usage': {'memory': 24820, 'cpu': 10406459}}, {'name': 'pod-8-d8754c67-77r5z', 'usage': {'memory': 127948, 'cpu': 174449619}}], 'type': 'worker', 'capacity': {'memory': 2165984, 'cpu': 2000000000}, 'usage': {'memory': 1445876, 'cpu': 699044843}}]

allocation_plan = get_refinelb_plan(nodes)
print(allocation_plan)
