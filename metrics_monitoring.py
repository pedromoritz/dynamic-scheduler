#!/usr/bin/env python3

import time
import kse as kse
from apscheduler.schedulers.background import BackgroundScheduler
import heapq
import sys

CSV_FILENAME = 'metrics_default_scheduler_'+sys.argv[1]+'_pods.csv'
INTERVAL = 60
COUNTER = 0

# workflow definitions
def scheduling_workflow():
  global COUNTER
  global INTERVAL
  global CSV_FILENAME 
  print('scheduling_workflow...')
  cluster = kse.Cluster()
  cluster.do_info_snapshot(CSV_FILENAME, COUNTER)
  COUNTER += INTERVAL

scheduling_workflow()
# creating a timer for workflow trigger
scheduler = BackgroundScheduler()
scheduler.add_job(scheduling_workflow, 'interval', seconds=INTERVAL)
scheduler.start()

# keeping script running
while True:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    scheduler.shutdown()
    break
