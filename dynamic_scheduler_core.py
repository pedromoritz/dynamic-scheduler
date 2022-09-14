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
        print(node.metadata.name)
        print(node.metadata.labels)
        print('')
        if 'node-role.kubernetes.io/control-plane' not in node.metadata.labels:
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

  def __init__(self, node_name, namespace):
    config.load_kube_config()
    self.node_name = node_name
    self.namespace = namespace

  @property
  def metrics(self):
    return self.get_metrics(self.node_name)

  def get_metrics(self, node_name):
    configuration = client.Configuration().get_default_copy()
    configuration.api_key_prefix['authorization'] = 'Bearer'
    api_client = client.ApiClient(configuration)
    custom_api = client.CustomObjectsApi(api_client)
    response = custom_api.list_cluster_custom_object('metrics.k8s.io', 'v1beta1', f'nodes/{node_name}')
    return {
      'name': node_name,
      'timestamp': response['timestamp'], # metric timestamp
      'usage': {
        'memory': int(response['usage']['memory'][:-2]), # memory in KB
        'cpu': int(response['usage']['cpu'][:-1]) # cpu in nanocores
      }
    }

  @property
  def pods(self):
    return self.get_pods(self.node_name, self.namespace)

  def get_pods(self, node_name, namespace):
    pods = []
    field_selector = 'spec.nodeName='+node_name+','+'metadata.namespace='+namespace+','+'spec.schedulerName=dynamic-scheduler'
    pods_list = client.CoreV1Api().list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
    for item in pods_list.items:
      if item.metadata.deletion_timestamp is None:
        pods.append({
          'name': item.metadata.name,
          'namespace': item.metadata.namespace
        })
    return pods

class Pod:

  def __init__(self, name, namespace):
    config.load_kube_config()
    self.name = name
    self.namespace = namespace

  @property
  def metrics(self):
    return get_metrics()

  def get_metrics(self):
    return []

  def evict(self):
    body = client.V1Eviction(metadata=client.V1ObjectMeta(name=self.name, namespace=self.namespace))
    try:
      client.CoreV1Api().create_namespaced_pod_eviction(name=self.name, namespace=self.namespace, body=body)
    except Exception as a:
      print ("Exception when calling CoreV1Api->create_namespaced_pod_eviction: %s\n" % a)
