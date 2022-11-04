#!/usr/bin/env python3

import random
import json
from kubernetes import client, config, watch
from apscheduler.schedulers.background import BackgroundScheduler as scheduler

config.load_kube_config()
v1 = client.CoreV1Api()

scheduler_name = "dynamic-scheduler"
namespace = "lab"

def get_available_nodes():
  ready_nodes = []
  nodes = v1.list_node().items
  for node in v1.list_node().items:
    for status in node.status.conditions:
      if 'node-role.kubernetes.io/control-plane' not in node.metadata.labels.keys():
        if status.status == "True" and status.type == "Ready":
          ready_nodes_item = {'name': None, 'capacity': {}}
          ready_nodes_item['name'] = node.metadata.name
          ready_nodes_item['capacity']['memory'] = int(node.status.capacity['memory'][:-2])
          ready_nodes_item['capacity']['cpu'] = int(node.status.capacity['cpu']) * 1000000000
          ready_nodes.append(ready_nodes_item)
  return ready_nodes

def scheduling_workflow(object, best_node_name, namespace):
  print("Scheduling " + object.metadata.name + " on node " + best_node_name)
  pod_scheduler(object.metadata.name, best_node_name, namespace)

def pod_scheduler(name, node, namespace="default"):
  target = client.V1ObjectReference(kind='Node', api_version='v1', name=node)
  meta = client.V1ObjectMeta(name=name)
  body = client.V1Binding(target=target, metadata=meta)
  try:
    v1.create_namespaced_binding(namespace=namespace, body=body, _preload_content=False)
  except Exception as a:
    print ("Exception when calling CoreV1Api->create_namespaced_binding: %s\n" % a)

def main():
  nodes = get_available_nodes()
  w = watch.Watch()
  rr_counter = 0
  for event in w.stream(v1.list_namespaced_pod, namespace):
    if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name and event['object'].spec.node_name == None:
      try:
        #target_node = nodes[random.randrange(len(nodes))]['name'] # RANDOM
        target_node = nodes[rr_counter]['name'] # ROUND ROBIN
        if rr_counter < len(nodes) - 1: 
          rr_counter =+ 1 
        else: 
          rr_counter = 0  
        scheduling_workflow(event['object'], target_node, namespace)
      except client.rest.ApiException as e:
        print(json.loads(e.body)['message'])
        
if __name__ == '__main__':
  main()


