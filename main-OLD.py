#!/usr/bin/env python3

import dynamic_scheduler_core as dscore
import time
from apscheduler.schedulers.background import BackgroundScheduler as scheduler

ds = dscore.DynamicScheduler()

def get_bad_node(metrics):
  return get_worst_memory_node(metrics)

def get_worst_memory_node(metrics):
  print("get_worst_memory_node")
  higher_node = sorted(metrics, key=lambda d: d['usage']['memory'], reverse=True)[0]
  #return higher_node if int(higher_node['usage']['memory']) > 2000000 else {}
  quotient = int(higher_node['usage']['memory']) / int(higher_node['capacity']['memory'])
  percent = round(quotient * 100, 2)
  if percent > 50:
    print("Bad node: " + higher_node['name'] + " => " + str(percent))
    return higher_node
  else:
    return {}

def eviction_workflow():
  global ds
  bad_node = get_bad_node(ds.get_metrics())
  pods_to_evict = ds.get_target_pods_on_node(bad_node)
  print(pods_to_evict)
  if len(pods_to_evict) > 0:
    pod_to_evict = pods_to_evict[0]
    pod_evictor(pod_to_evict['name'], pod_to_evict['namespace'])

def main():
  #sch = scheduler()
  #sch.add_job(eviction_workflow, 'interval', seconds=2)
  #sch.start()
  #while True:
  #  time.sleep(2)

if __name__ == '__main__':
  main()