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
            node_memory = Utils.get_memory_integer(response['usage']['memory'])
            node_cpu = Utils.get_cpu_integer(response['usage']['cpu'])
          ready_nodes.append({
            'name': node.metadata.name,
            'pods': self.get_pods_from_node(node.metadata.name),
            'type': 'master' if 'node-role.kubernetes.io/master' in node.metadata.labels else 'worker',
            'capacity': {
              'memory': Utils.get_memory_integer(node.status.capacity['memory']), # memory in KB
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
        unready_pods.append({
          'name': pod.metadata.generate_name,
          'status': pod.status.phase
        })
    return unready_pods

  def set_allocation_plan(self, allocation_plan, csv_filename = '', timestamp = 0):
    for pod_name in allocation_plan:
      target_node = allocation_plan[pod_name]      
      host_node = self.get_node_from_pod(pod_name)
      if (target_node != host_node):
        pod = Pod(pod_name)
        if host_node != None:
          pod.evict()
          pod = Pod(pod_name[:-5])
          if csv_filename != '':
            self.do_info_migrations(csv_filename, [timestamp, pod_name[:-6], host_node, target_node])
        pod.schedule(target_node)
    return True

  def do_info_migrations(self, csv_filename, data):
    Utils.write_file(csv_filename, ','.join(map(str, data)))

  def get_node_from_pod(self, pod_name):
    for pod in client.CoreV1Api().list_namespaced_pod('lab').items:
      if pod.metadata.name == pod_name or pod.metadata.generate_name == pod_name:
        return pod.spec.node_name
    return ''

  def do_info_snapshot(self, csv_filename, timestamp, nodes):
    info = {
      'header': [],
      'data': []
    }
    info['header'].append('timestamp')
    for node in nodes:
      info['header'].append(node['name']+'_pod_amount') # amount of pods on node
      info['header'].append(node['name']+'_memory') # usage of memory on node
      info['header'].append(node['name']+'_cpu') # usage of cpu on node
      info['data'].append(len(node['pods']))
      info['data'].append(node['usage']['memory'])
      info['data'].append(node['usage']['cpu'])
    if timestamp == 0:
      Utils.write_file(csv_filename, ','.join(map(str, info['header'])), 'w')
    Utils.write_file(csv_filename, str(timestamp)+','+','.join(map(str, info['data'])))
    return True

# Node class
class Node:
  def __init__(self):
    return None

  def get_pods(self, name):
    pods = []
    field_selector = 'spec.nodeName='+name+','+'metadata.namespace=lab'
    pods_list_raw = client.CoreV1Api().list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
    pods_list = list(map(lambda n: n.metadata.name, pods_list_raw.items))
    all_pods_list = Utils.call_api('namespaces/lab/pods')
    for item in all_pods_list['items']:
      if item['metadata'].get('deletion_timestamp') is None and item['metadata']['name'] in pods_list:
        pod_memory = Utils.get_memory_integer(item['containers'][0]['usage']['memory'])
        pod_cpu = Utils.get_cpu_integer(item['containers'][0]['usage']['cpu'])
        pods.append({
          'name': item['metadata']['name'],
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
          print("schedule exception:")
          print(json.loads(e.body)['message'])
 
# Utils class
class Utils:
  def call_api(path):
    print(path)
    max_attempts = 3
    retry_delay = 1
    for attempt in range(max_attempts):
      print(str(attempt) + ' try...')
      try:
        configuration = client.Configuration().get_default_copy()
        configuration.api_key_prefix['authorization'] = 'Bearer'
        api_client = client.ApiClient(configuration)
        custom_api = client.CustomObjectsApi(api_client)
        response = custom_api.list_cluster_custom_object('metrics.k8s.io', 'v1beta1', path)
        return response
      except Exception as a:
        print("call_api exception: %s\n" % path)
        print(a.body)
        time.sleep(retry_delay) 
    return {}

  def write_file(filename, record, type = 'a'):
    output_file = open('results/'+filename, mode=type)
    output_file.write(record + '\n')
    output_file.close()

  def get_memory_integer(memory_string):
    memory_integer = 0
    unit = memory_string[-2:]
    if unit == 'Ki':
      memory_integer = int(memory_string[:-2])
    if unit == 'Mi':
      memory_integer = int(memory_string[:-2]) * 1024
    return memory_integer

  def get_cpu_integer(cpu_string):
    cpu_integer = 0
    unit = cpu_string[-1:]
    if unit == 'n':
      cpu_integer = int(cpu_string[:-1])
    else:
      cpu_integer = int(cpu_string[:-1]) * 1000
    return cpu_integer
