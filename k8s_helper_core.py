from kubernetes import client, config, watch
import json

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
        if 'node-role.kubernetes.io/control-plane' not in node.metadata.labels:
          response = Utils.call_api(f'nodes/{node.metadata.name}')
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

  @property
  def pending_pods(self):
    return self.get_pending_pods()

  def get_pending_pods(self):
    pending_pods = []
    for pod in client.CoreV1Api().list_namespaced_pod('default').items:
      if pod.status.phase == "Pending" and """pod.spec.scheduler_name == 'dynamic-scheduler' and""" pod.spec.node_name == None:
        pending_pods.append({
          'name': pod.metadata.generate_name
        })
    return pending_pods

  @property
  def not_ready_pods(self):
    return self.get_not_ready_pods()

  def get_not_ready_pods(self):
    not_ready_pods = []
    for pod in client.CoreV1Api().list_namespaced_pod('default').items:
      if pod.status.phase != 'Running' """and pod.spec.scheduler_name == 'dynamic-scheduler'""":
        not_ready_pods.append({
          'name': pod.metadata.generate_name,
          'status': pod.status.phase
        })
    return not_ready_pods

  def get_node_from_pod(self, pod_name):
    for pod in client.CoreV1Api().list_namespaced_pod('default').items:
      if pod.metadata.name == pod_name or pod.metadata.generate_name == pod_name:
        return pod.spec.node_name
    return ''

  def set_allocation_plan(self, allocation_plan):
    for pod_name in allocation_plan:
      target_node = allocation_plan[pod_name]      
      host_node = self.get_node_from_pod(pod_name)
      print('------------------')
      print('pod_name: ' + pod_name)
      print('host_node: ' + str(host_node))
      if (target_node != host_node):
        pod = Pod(pod_name)
        if host_node != None:
          pod.evict()
          pod = Pod(pod_name[:-5])
        print('target_node: ' + target_node)
        pod.schedule(target_node)
    return True

class Node:

  def __init__(self, name):
    config.load_kube_config()
    self.name = name

  @property
  def pods(self):
    return self.get_pods(self.name)

  def get_pods(self, name):
    pods = []
    field_selector = 'spec.nodeName='+name+','+'metadata.namespace=default'
    pods_list = client.CoreV1Api().list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
    for item in pods_list.items:
      if item.metadata.deletion_timestamp is None:
        response = Utils.call_api(f'namespaces/default/pods/{item.metadata.name}')
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

class Pod:

  def __init__(self, name):
    config.load_kube_config()
    self.name = name

  @property
  def metrics(self):
    return self.get_metrics(self.name)

  def get_metrics(self, name):
    response = Utils.call_api(f'namespaces/default/pods/{name}')
    if response:
      print(response)
      return {
        'name': name,
        'timestamp': response['timestamp'], # metric timestamp
        'containers': response['containers']
      }
    else:
      return {}

  def evict(self):
    body = client.V1Eviction(metadata=client.V1ObjectMeta(name=self.name, namespace='default'))
    try:
      client.CoreV1Api().create_namespaced_pod_eviction(name=self.name, namespace='default', body=body)
    except Exception as a:
      print ("Exception when calling CoreV1Api->create_namespaced_pod_eviction: %s\n" % a)
    return True

  def schedule(self, node_name):
    pod_to_schedule = self.name
    print(pod_to_schedule)
    w = watch.Watch()
    for event in w.stream(client.CoreV1Api().list_namespaced_pod, 'default'):
      pod = event['object']
      if pod.status.phase == "Pending" and """pod.spec.scheduler_name == 'dynamic-scheduler' and""" pod.spec.node_name == None and pod.metadata.generate_name == pod_to_schedule:
        try:
          target = client.V1ObjectReference(kind='Node', api_version='v1', name=node_name)
          meta = client.V1ObjectMeta(name=pod.metadata.name)
          body = client.V1Binding(target=target, metadata=meta)
          try:
            client.CoreV1Api().create_namespaced_binding(namespace='default', body=body, _preload_content=False)
            w.stop()
          except Exception as a:
            print ("Exception when calling CoreV1Api->create_namespaced_binding: %s\n" % a)
        except client.rest.ApiException as e:
          print(json.loads(e.body)['message'])

    
