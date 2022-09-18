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
  for node_item in nodes:
    node = dscore.Node(node_item['name'], namespace)
    node_item['usage'] = node.metrics['usage']
    print(node_item['name'] + ' - ' + str(node_item['usage']['memory']))
    pods = node.pods
    for pod_item in pods:
      print(pod_item['name'])
      pod_object = dscore.Pod(pod_item['name'], namespace)
      print(pod_object.metrics)
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
