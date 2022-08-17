import json
from kubernetes import client, config, watch

class Cluster:

  def __init__(self):
    config.load_kube_config()
    self.v1 = client.CoreV1Api()
    self.scheduler_name = 'dynamic-scheduler'
    self.namespace = 'lab1'
    self.schedule_new_pods()

  @property
  def nodes(self):
    return self.get_metrics()

  def get_available_nodes(self):
    ready_nodes = []
    nodes = self.v1.list_node().items
    for node in self.v1.list_node().items:
      for status in node.status.conditions:
        if 'node-role.kubernetes.io/control-plane' not in node.metadata.labels.keys():
          if status.status == "True" and status.type == "Ready":
            ready_nodes_item = {'name': None, 'capacity': {}}
            ready_nodes_item['name'] = node.metadata.name
            ready_nodes_item['capacity']['memory'] = int(node.status.capacity['memory'][:-2])
            ready_nodes_item['capacity']['cpu'] = int(node.status.capacity['cpu']) * 1000000000
            ready_nodes.append(ready_nodes_item)
    return ready_nodes

  def get_metrics(self):
    available_nodes = self.get_available_nodes()
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

  @nodes.setter
  def nodes(self, nodes_list):
    print("setter method called")
    #self._nodes = nodes_list

  def pod_scheduler(self, name, node, namespace="default"):
    target = client.V1ObjectReference(kind='Node', api_version='v1', name=node)
    meta = client.V1ObjectMeta(name=name)
    body = client.V1Binding(target=target, metadata=meta)
    try:
      self.v1.create_namespaced_binding(namespace=namespace, body=body, _preload_content=False)
    except Exception as a:
      print ("Exception when calling CoreV1Api->create_namespaced_binding: %s\n" % a)

  def scheduling_workflow(self, object, best_node_name, namespace):
    print("Scheduling " + object.metadata.name + " on node " + best_node_name)
    self.pod_scheduler(object.metadata.name, best_node_name, namespace)

  def schedule_new_pods(self):
    # creating a watch to verify pending pods and binding them to a node
    w = watch.Watch()
    for event in w.stream(self.v1.list_namespaced_pod, self.namespace):
      if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == self.scheduler_name and event['object'].spec.node_name == None:
        try:
          self.scheduling_workflow(event['object'], 'ppgcc-m02', self.namespace)
        except client.rest.ApiException as e:
          print(json.loads(e.body)['message'])

class Node:

  def __init__(self):
    config.load_kube_config()
    self.v1 = client.CoreV1Api()
    self.pods = []

  @property
  def nodes(self):
    self.get_target_pods_on_node('ppgcc-m02')
    return self.get_metrics()

  def get_target_pods_on_node(self, bad_node):
    pods = []
    if len(bad_node) > 0:
      field_selector = 'spec.nodeName='+bad_node+','+'metadata.namespace=lab1'
      pods_list = self.v1.list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
      for item in pods_list.items:
        pod = {}
        pod['name'] = item.metadata.name
        pod['namespace'] = item.metadata.namespace
        pods.append(pod)
    print(pods)
    #return pods


#Class Node {
#  private String name;
#  private NodeMetrics metrics;
#  private List <Pod> pods;
#  Pod remove_pod();
#  add_pod(Pod p);
#  string get_name();
#  void set_name(String name);
#  NodeMetrics get_metrics();
#  List get_pods();
#}


