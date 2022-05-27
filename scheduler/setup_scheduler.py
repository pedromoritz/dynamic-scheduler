#!/usr/bin/env python3

import json

from kubernetes import client, config, watch
from apscheduler.schedulers.background import BackgroundScheduler as scheduler

config.load_kube_config()
v1 = client.CoreV1Api()

scheduler_name = "ppgcc_balancer"
namespace = "lab1"

def get_available_nodes():
  ready_nodes = []
  nodes = v1.list_node().items
  for node in v1.list_node().items:
    for status in node.status.conditions:
      if status.status == "True" and status.type == "Ready":
        ready_nodes_item = {'name': None, 'capacity': {}}
        ready_nodes_item['name'] = node.metadata.name
        ready_nodes_item['capacity']['memory'] = node.status.capacity['memory']
        ready_nodes_item['capacity']['cpu'] = node.status.capacity['cpu']
        ready_nodes.append(ready_nodes_item)
  return ready_nodes

def pod_scheduler(name, node, namespace="default"):
  target = client.V1ObjectReference(kind = 'Node', api_version = 'v1', name = node)
  meta = client.V1ObjectMeta(name = name)
  body = client.V1Binding(target = target, metadata = meta)
  try:
    client.CoreV1Api().create_namespaced_binding(namespace=namespace, body=body)
  except ValueError:
    print("error")

def main():
  get_available_nodes()
  w = watch.Watch()
  for event in w.stream(v1.list_namespaced_pod, namespace):
    if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name:
      try:
        print("Scheduling " + event['object'].metadata.name)
        res = pod_scheduler(event['object'].metadata.name, 'ppgcc-m02', namespace)
      except client.rest.ApiException as e:
        print(json.loads(e.body)['message'])

if __name__ == '__main__':
  main()


