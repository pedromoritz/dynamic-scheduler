from kubernetes import client, config, watch
import json

class Cluster:

  def __init__(self):
    config.load_kube_config()

  @property
  def nodes(self):
    return self.get_nodes()

  def get_nodes(self):
    ready_nodes = []
    for node in client.CoreV1Api().list_node().items:
      last_condition = node.status.conditions[-1]     
      if last_condition.status == 'True' and last_condition.type == 'Ready' and last_condition.reason == 'KubeletReady':
        if 'node-role.kubernetes.io/master' not in node.metadata.labels:
          ready_nodes.append({
            'name': node.metadata.name,
            'type': 'master' if 'node-role.kubernetes.io/master' in node.metadata.labels else 'worker',
            'capacity': {
              'memory': int(node.status.capacity['memory'][:-2]), # memory in KB
              'cpu': int(node.status.capacity['cpu']) * 1000000000 # cpu in nanocores
            }
          })
    return ready_nodes

class Node:

  def __init__(self, node_name):
    config.load_kube_config()
    self.node_name = node_name

  @property
  def metrics(self):
    return self.get_metrics(self.node_name)

  def get_metrics(self, node_name):
    configuration = client.Configuration()
    configuration.api_key_prefix['authorization'] = 'Bearer'
    api_client = client.ApiClient(configuration)
    custom_api = client.CustomObjectsApi(api_client)
    response = custom_api.list_cluster_custom_object('metrics.k8s.io', 'v1beta1', f'nodes/{node_name}')
    node_metrics = {
      'name': node_name,
      'timestamp': response['timestamp'], # metric timestamp
      'usage': {
        'memory': int(response['usage']['memory'][:-2]), # memory in KB
        'cpu': int(response['usage']['cpu'][:-1]) # cpu in nanocores
      }
    }
    return node_metrics

  @property
  def pods(self):
    return self.get_pods(self.node_name)

  def get_pods(self, node_name):
    pods = []
    field_selector = f'spec.nodeName={node_name}'
    pods_list = client.CoreV1Api().list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
    for item in pods_list.items:
      pod = {
        'name': item.metadata.name,
        'namespace': item.metadata.namespace,
      }
      pods.append(pod)
    return pods

class Pod:

  def __init__(self):
    config.load_kube_config()

  @property
  def metrics(self):
    return get_metrics()

  def get_metrics(self):
    return []
