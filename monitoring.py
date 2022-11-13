#!/usr/bin/env python3

from datetime import datetime
import csv
import json
import time
import k8s_helper_core as khc
from apscheduler.schedulers.background import BackgroundScheduler

namespace = 'lab'

def read_cluster_data_workflow():
  cluster = khc.Cluster()
  nodes = cluster.nodes
  print('----------------------------------------')
  for nodes_item in nodes:
    percentual_memory_usage = (nodes_item['usage']['memory'] / nodes_item['capacity']['memory']) * 100
    print('NODE ' + nodes_item['name'] + ' - ' + str(round(nodes_item['usage']['memory'] / 1024, 1)) + 'MB (' + str(round(percentual_memory_usage, 2)) + '%) - ' + str(nodes_item['usage']['cpu']))
    node = khc.Node(nodes_item['name'], namespace)
    pods = node.pods
    for pods_item in pods:
      print('POD ' + pods_item['name'] + ' - ' + str(round(pods_item['usage']['memory'] / 1024, 1)) + 'MB' + ' - ' + str(pods_item['usage']['cpu']))
    print('')  

# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(read_cluster_data_workflow, 'interval', seconds=5)
scheduler.start()

#csvfile = open('results-' + str(datetime.now().strftime('%Y%d%m')) + '.csv', 'w', 1)
#3writer = csv.writer(csvfile)
#fieldnames = ['timestamp', 'ppgcc-m02 memory', 'ppgcc-m03 memory']
#writer.writerow(fieldnames)

#ts0 = datetime.timestamp(datetime.now())

read_cluster_data_workflow()

# keeping script running
while True:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    #csvfile.close()
    scheduler.shutdown()
    break
