# Kubernetes Scheduling Extension

from kubernetes import client, config, watch
import json
import time

# Cluster class 
class Cluster:
  def __init__(self):
    config.load_kube_config()
    self.node = Node()
 
  def get_pods_from_node(self, name):
    return self.node.get_pods(name)
 
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

  def get_pending_pods(self):
    pending_pods = []
    for pod in client.CoreV1Api().list_namespaced_pod('lab').items:
      if pod.status.phase == "Pending" and pod.spec.node_name == None:
        pending_pods.append({
          'name': pod.metadata.generate_name
        })
    return pending_pods

  def get_unready_pods(self):
    unready_pods = []
    for pod in client.CoreV1Api().list_namespaced_pod('lab').items:
      if pod.status.phase != 'Running':
        not_ready_pods.append({
          'name': pod.metadata.generate_name,
          'status': pod.status.phase
        })
    return unready_pods

  def set_allocation_plan(self, allocation_plan):
    for pod_name in allocation_plan:
      target_node = allocation_plan[pod_name]      
      host_node = self.get_node_from_pod(pod_name)
      if (target_node != host_node):
        pod = Pod(pod_name)
        if host_node != None:
          pod.evict()
          pod = Pod(pod_name[:-5])
        pod.schedule(target_node)
    return True

  def get_node_from_pod(self, pod_name):
    for pod in client.CoreV1Api().list_namespaced_pod('lab').items:
      if pod.metadata.name == pod_name or pod.metadata.generate_name == pod_name:
        return pod.spec.node_name
    return ''

# Node class
class Node:
  def __init__(self):
    print('')

  def get_pods(self, name):
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

# Pod class
class Pod:
  def __init__(self, name):
    config.load_kube_config()
    self.name = name

  def get_metrics(self, name):
    response = Utils.call_api('namespaces/lab/pods/'+name)
    if response:
      return {
        'name': name,
        'timestamp': response['timestamp'], # metric timestamp
        'containers': response['containers']
      }
    else:
      return {}

  def evict(self):
    body = client.V1Eviction(metadata=client.V1ObjectMeta(name=self.name, namespace='lab'))
    try:
      client.CoreV1Api().create_namespaced_pod_eviction(name=self.name, namespace='lab', body=body)
    except Exception as a:
      print ("Exception when calling CoreV1Api->create_namespaced_pod_eviction: %s\n" % a)
    return True

  def schedule(self, node_name):
    pod_to_schedule = self.name
    w = watch.Watch()
    for event in w.stream(client.CoreV1Api().list_namespaced_pod, 'lab'):
      pod = event['object']
      if pod.status.phase == "Pending" and pod.spec.node_name == None and pod.metadata.generate_name == pod_to_schedule:
        try:
          target = client.V1ObjectReference(kind='Node', api_version='v1', name=node_name)
          meta = client.V1ObjectMeta(name=pod.metadata.name)
          body = client.V1Binding(target=target, metadata=meta)
          try:
            client.CoreV1Api().create_namespaced_binding(namespace='lab', body=body, _preload_content=False)
            w.stop()
          except Exception as a:
            print ("Exception when calling CoreV1Api->create_namespaced_binding: %s\n" % a)
        except client.rest.ApiException as e:
          print(json.loads(e.body)['message'])
 
# Utils class
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

# Testing classes

cluster = Cluster()
nodes = cluster.get_nodes()
print(nodes)

pending_pods = cluster.get_pending_pods()
print(pending_pods)

unready_pods = cluster.get_unready_pods()
print(unready_pods)

pods = cluster.get_pods_from_node(nodes[0]['name'])
print(pods)



