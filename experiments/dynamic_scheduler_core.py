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
          node_metrics_info = Utils.call_api(f'nodes/{node.metadata.name}')
          ready_nodes.append({
            'name': node.metadata.name,
            'type': 'master' if 'node-role.kubernetes.io/master' in node.metadata.labels else 'worker',
            'capacity': {
              'memory': int(node.status.capacity['memory'][:-2]), # memory in KB
              'cpu': int(node.status.capacity['cpu']) * 1000000000 # cpu in nanocores
            },
            'usage': {
              'memory': int(node_metrics_info['usage']['memory'][:-2]), # memory in KB
              'cpu': int(node_metrics_info['usage']['cpu'][:-1]) # cpu in nanocores
            }
          })
    return ready_nodes

  def set_allocation_plan(self, allocation_plan):
    for pod_allocation_plan in allocation_plan:
      #print(pod_allocation_plan)
      #current_pod = Pod(pod_allocation_plan['name'], pod_allocation_plan['namespace'])
      #print(current_pod.metrics)
      if (pod_allocation_plan['source_node'] != pod_allocation_plan['target_node']):
        print('Rescheduling ' + pod_allocation_plan['name'] + ' on node ' + pod_allocation_plan['target_node'])
        pod = Pod(pod_allocation_plan['name'], pod_allocation_plan['namespace'])
        pod.evict()
        pod.schedule(pod_allocation_plan['target_node'])
    return True

class Node:

  def __init__(self, name, namespace):
    config.load_kube_config()
    self.name = name
    self.namespace = namespace

  @property
  def pods(self):
    return self.get_pods(self.name, self.namespace)

  def get_pods(self, name, namespace):
    pods = []
    field_selector = 'spec.nodeName='+name+','+'metadata.namespace='+namespace+','+'spec.schedulerName=dynamic-scheduler'
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
    return self.get_metrics(self.name)

  def get_metrics(self, name):
    response = Utils.call_api(f'namespaces/{self.namespace}/pods/{name}')
    if response:
      return {
        'name': name,
        'timestamp': response['timestamp'], # metric timestamp
        'containers': response['containers']
      }
    else:
      return {}

  def evict(self):
    body = client.V1Eviction(metadata=client.V1ObjectMeta(name=self.name, namespace=self.namespace))
    try:
      client.CoreV1Api().create_namespaced_pod_eviction(name=self.name, namespace=self.namespace, body=body)
    except Exception as a:
      print ("Exception when calling CoreV1Api->create_namespaced_pod_eviction: %s\n" % a)
    return True

  def schedule(self, node_name):
    pod_to_schedule = self.name[0:-5]
    w = watch.Watch()
    for event in w.stream(client.CoreV1Api().list_namespaced_pod, self.namespace):
      pod = event['object']
      if pod.status.phase == "Pending" and pod.spec.scheduler_name == 'dynamic-scheduler' and pod.spec.node_name == None and pod.metadata.generate_name == pod_to_schedule:
        try:
          target = client.V1ObjectReference(kind='Node', api_version='v1', name=node_name)
          meta = client.V1ObjectMeta(name=pod.metadata.name)
          body = client.V1Binding(target=target, metadata=meta)
          try:
            client.CoreV1Api().create_namespaced_binding(namespace=self.namespace, body=body, _preload_content=False)
            w.stop()
          except Exception as a:
            print ("Exception when calling CoreV1Api->create_namespaced_binding: %s\n" % a)
        except client.rest.ApiException as e:
          print(json.loads(e.body)['message'])

    