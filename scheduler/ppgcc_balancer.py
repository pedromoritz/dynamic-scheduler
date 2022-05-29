#!/usr/bin/env python3

import json

from kubernetes import client, config, watch
from apscheduler.schedulers.background import BackgroundScheduler as scheduler

config.load_kube_config()
v1 = client.CoreV1Api()

scheduler_name = "ppgcc_balancer"
namespace = "lab1"
best_node = {}
bad_node = {}

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

def pod_scheduler(name, node, namespace="default"):
  target = client.V1ObjectReference(kind='Node', api_version='v1', name=node)
  meta = client.V1ObjectMeta(name=name)
  body = client.V1Binding(target=target, metadata=meta)
  try:
    v1.create_namespaced_binding(namespace=namespace, body=body, _preload_content=False)
  except Exception as a:
    print ("Exception when calling CoreV1Api->create_namespaced_binding: %s\n" % a)

def pod_evictor(name, namespace="default"):
  body = client.V1beta1Eviction(metadata=client.V1ObjectMeta(name=name, namespace=namespace))
  try:
    v1.create_namespaced_pod_eviction(name=name, namespace=namespace, body=body)
  except Exception as a:
    print ("Exception when calling CoreV1Api->create_namespaced_pod_eviction: %s\n" % a)

def get_metrics():
  available_nodes = get_available_nodes()
  api_client = client.ApiClient()
  ret_metrics = api_client.call_api('/apis/metrics.k8s.io/v1beta1/nodes', 'GET', auth_settings=['BearerToken'], response_type='json', _preload_content=False)
  response = ret_metrics[0].data.decode('utf-8')
  response_obj = json.loads(response)
  metrics_items_raw = response_obj["items"]
  metrics_items = {}
  for item in metrics_items_raw:  
    new_item = {}
    new_item['timestamp'] = item['timestamp']
    new_item['memory'] = int(item['usage']['memory'][:-2]) # memory in KB
    new_item['cpu'] = int(item['usage']['cpu'][:-1]) # cpu in nanocores
    metrics_items[item['metadata']['name']] = new_item
  for node in available_nodes:
    node['usage'] = {}
    node['usage']['memory'] = metrics_items[node['name']]['memory']
    node['usage']['cpu'] = metrics_items[node['name']]['cpu']
  return available_nodes

def get_best_node(available_nodes):
  return get_best_memory_node(available_nodes)

def get_best_memory_node(available_nodes):
  return sorted(available_nodes, key=lambda d: d['usage']['memory'])[0]

def scheduling_workflow(object, best_node_name, namespace):
  print("Scheduling " + object.metadata.name + " on node " + best_node_name)
  pod_scheduler(object.metadata.name, best_node_name, namespace)

def eviction_workflow():
  bad_node = get_bad_node(get_metrics())
  pods_to_evict = get_target_pods_on_node(bad_node)
  if len(pods_to_evict) > 0:
    pod_to_evict = pods_to_evict[0]
    pod_evictor(pod_to_evict['name'], pod_to_evict['namespace'])

def get_bad_node(available_nodes):
  return get_worst_memory_node(available_nodes)

def get_worst_memory_node(available_nodes):
  higher_node = sorted(available_nodes, key=lambda d: d['usage']['memory'], reverse=True)[0]
  return higher_node if int(higher_node['usage']['memory']) > 2000000 else {}

def get_target_pods_on_node(bad_node):
  pods = []
  if len(bad_node) > 0:
    global scheduler_name
    field_selector = 'spec.nodeName='+bad_node['name']+','+'metadata.namespace=lab1'+','+'spec.schedulerName='+scheduler_name
    pods_list = v1.list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
    for item in pods_list.items:
      pod = {}
      pod['name'] = item.metadata.name
      pod['namespace'] = item.metadata.namespace
      pods.append(pod)
  return pods

def main():
  # creating a scheduler to query metrics server every x seconds
  sch = scheduler()
  sch.add_job(eviction_workflow, 'interval', seconds=5)
  sch.start()
  # creating a watch to verify pending pods and binding them to a node
  w = watch.Watch()
  for event in w.stream(v1.list_namespaced_pod, namespace):
    if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name and event['object'].spec.node_name == None:
      try:
        scheduling_workflow(event['object'], get_best_node(get_metrics())['name'], namespace)
      except client.rest.ApiException as e:
        print(json.loads(e.body)['message'])

if __name__ == '__main__':
  main()


