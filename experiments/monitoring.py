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
    print('---> ' + nodes_item['name'] + ' - ' + str(nodes_item['usage']['memory']) + 'KB - ' + str(round(percentual_memory_usage, 2)) + '%')
    print('')
    node = dscore.Node(nodes_item['name'], namespace)
    pods = node.pods
    for pods_item in pods:
      print('     ' + pods_item['name'], end=' ')
      pod_object = dscore.Pod(pods_item['name'], namespace)
      pod_metrics = pod_object.metrics
      if 'containers' in pod_metrics:
        for containers_item in pod_metrics['containers']:
          print(' -> ' + containers_item['name'] + ' - ' + containers_item['usage']['memory'][:-2] + 'KB')
      print('')
    print('')  
  #ppgcc_m02, ppgcc_m03 = nodes
  #ppgcc_m02 = nodes
  #timestamp = datetime.timestamp(datetime.now()) - ts0
  #writer.writerow(ppgcc_m02)
  #writer.writerow([round(timestamp, 3), ppgcc_m02['usage']['memory'], ppgcc_m03['usage']['memory']])
  #writer.writerow([round(timestamp, 3), ppgcc_m02['usage']['memory']])
  #ppgcc_m02_usage_memory = ppgcc_m02['usage']['memory']
  #writer.writerow([ppgcc_m02_usage_memory])

# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(read_cluster_data_workflow, 'interval', seconds=5)
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
