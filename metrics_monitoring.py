#!/usr/bin/env python3

import time
import k8s_scheduling_extension as kse
from apscheduler.schedulers.background import BackgroundScheduler

def save_log_record(nodes, pods):
  csv_record = str(int(time.time())) + ',' \
    + str(nodes[0]['usage']['memory']) + ',' \
    + str(nodes[1]['usage']['memory']) + ',' \
    + str(nodes[2]['usage']['memory']) + ',' \
    + str(pods[0]['usage']['memory']) + ',' \
    + str(pods[1]['usage']['memory']) + ',' \
    + str(pods[2]['usage']['memory']) + ',' \
    + str(pods[3]['usage']['memory']) + ',' \
    + str(pods[4]['usage']['memory']) + ',' \
    + str(pods[5]['usage']['memory'])
  metrics_file = open('metrics_default_scheduler_memory.csv', mode='a')
  metrics_file.write(csv_record + '\n')
  metrics_file.close()

# workflow definitions
def scheduling_workflow():
  cluster = kse.Cluster()
  nodes = cluster.nodes
  pods = []
  for node_item in nodes:
    node = kse.Node(node_item['name'])
    pods = pods + node.pods
  save_log_record(nodes, pods)

metrics_file = open('metrics_default_scheduler_memory.csv', mode='w')
metrics_file.write('timestamp,node1,node2,node3,pod1,pod2,pod3,pod4,pod5,pod6' + '\n')
metrics_file.close()

scheduling_workflow()
# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(scheduling_workflow, 'interval', seconds=60)
scheduler.start()

# keeping script running
while True:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    scheduler.shutdown()
    break
