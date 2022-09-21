#!/usr/bin/env python3

from datetime import datetime
import csv
import json
import time
import dynamic_scheduler_core as dscore
from apscheduler.schedulers.background import BackgroundScheduler

namespace = 'lab'

# workflow definitions
def read_cluster_data_workflow():

  cluster = dscore.Cluster()
  nodes = cluster.nodes

  print('----------------------------------------')
  for nodes_item in nodes:
    percentual_memory_usage = (nodes_item['usage']['memory'] / nodes_item['capacity']['memory']) * 100
    print('---> ' + nodes_item['name'] + ' - ' + str(nodes_item['usage']['memory']) + ' - ' + str(round(percentual_memory_usage, 2)) + '%')
    print('')
    node = dscore.Node(nodes_item['name'], namespace)
    pods = node.pods
    for pods_item in pods:
      print('     ' + pods_item['name'])
      pod_object = dscore.Pod(pods_item['name'], namespace)
      pod_metrics = pod_object.metrics
      if 'containers' in pod_metrics:
        for containers_item in pod_metrics['containers']:
          print('     ' + containers_item['name'] + ' - ' + containers_item['usage']['memory'])
      print('')

  ppgcc_m02, ppgcc_m03 = nodes
  timestamp = datetime.timestamp(datetime.now()) - ts0
  writer.writerow([round(timestamp, 3), ppgcc_m02['usage']['memory'], ppgcc_m03['usage']['memory']])

# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(read_cluster_data_workflow, 'interval', seconds=10)
scheduler.start()

csvfile = open('results-' + str(datetime.now().strftime('%Y%d%m')) + '.csv', 'w', 1)
writer = csv.writer(csvfile)
fieldnames = ['timestamp', 'ppgcc-m02 memory', 'ppgcc-m03 memory']
writer.writerow(fieldnames)

ts0 = datetime.timestamp(datetime.now())

read_cluster_data_workflow()

# keeping script running
while True:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    csvfile.close()
    scheduler.shutdown()
    break
