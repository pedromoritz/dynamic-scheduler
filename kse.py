# Kubernetes Scheduling Extension

from kubernetes import client, config, watch
import json
import time

class Utils:
  def call_api(path):
    try:
      configuration = client.Configuration().get_default_copy()
      configuration.api_key_prefix['authorization'] = 'Bearer'
      api_client = client.ApiClient(configuration)
      custom_api = client.CustomObjectsApi(api_client)
      return custom_api.list_cluster_custom_object('metrics.k8s.io', 'v1beta1', path)
    except Exception as a:
      return {}

class Pod:
  def __init__(self):
    print('')

class Node:
  def __init__(self):
    print('')

  def get_pods_from_node(self, name):
    pods = []
    field_selector = 'spec.nodeName='+name+','+'metadata.namespace=lab'
    pods_list = client.CoreV1Api().list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
    for item in pods_list.items:
      if item.metadata.deletion_timestamp is None:
        response = Utils.call_api('namespaces/lab/pods/'+item.metadata.name)
        pod_memory = 0
        pod_cpu = 0
        if response and response['containers']:
          pod_memory = int(response['containers'][0]['usage']['memory'][:-2])
          pod_cpu = int(response['containers'][0]['usage']['cpu'][:-1])
        pods.append({
          'name': item.metadata.name,
          'usage': {
            'memory': pod_memory, # memory in KB
            'cpu': pod_cpu # cpu in nanocores
          }
        })
    return pods
 
class Cluster:
  def __init__(self):
    config.load_kube_config()
    self.node = Node()
 
  def get_pods_from_node(self, name):
    return self.node.get_pods_from_node(name)
 
  def get_nodes(self):
    ready_nodes = []
    for node in client.CoreV1Api().list_node().items:
      last_condition = node.status.conditions[-1]     
      if last_condition.status == 'True' and last_condition.type == 'Ready' and last_condition.reason == 'KubeletReady':
        if 'node-role.kubernetes.io/control-plane' not in node.metadata.labels:
          response = Utils.call_api('nodes/'+node.metadata.name)
          node_memory = 0
          node_cpu = 0
          if response and response['usage']:
            node_memory = int(response['usage']['memory'][:-2]) 
            node_cpu = int(response['usage']['cpu'][:-1])
          ready_nodes.append({
            'name': node.metadata.name,
            'type': 'master' if 'node-role.kubernetes.io/master' in node.metadata.labels else 'worker',
            'capacity': {
              'memory': int(node.status.capacity['memory'][:-2]), # memory in KB
              'cpu': int(node.status.capacity['cpu']) * 1000000000 # cpu in nanocores
            },
            'usage': {
              'memory': node_memory, # memory in KB
              'cpu': node_cpu # cpu in nanocores
            }
          })
    return ready_nodes 

cluster = Cluster()
nodes = cluster.get_nodes()
print(nodes)

pods = cluster.get_pods_from_node(nodes[0]['name'])
print(pods)

