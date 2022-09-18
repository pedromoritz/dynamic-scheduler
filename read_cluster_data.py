#!/usr/bin/env python3

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
    node = dscore.Node(nodes_item['name'], namespace)
    nodes_item['usage'] = node.metrics['usage']
    print(nodes_item['name'] + ' - ' + str(nodes_item['usage']['memory']))
    print('')
    pods = node.pods
    for pods_item in pods:
      print(pods_item['name'])
      pod_object = dscore.Pod(pods_item['name'], namespace)
      pod_metrics = pod_object.metrics
      for containers_item in pod_metrics['containers']:
        print(containers_item)
      print('')
    print('')

# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(read_cluster_data_workflow, 'interval', seconds=5)
scheduler.start()

# keeping script running
while True:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    scheduler.shutdown()
    break
