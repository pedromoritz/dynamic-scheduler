from kubernetes import client, config, watch

class Cluster:

  def __init__(self):
    config.load_kube_config()
    self.v1 = client.CoreV1Api()

  @property
  def nodes(self):
    return self.get_nodes()

  def get_nodes(self):
    ready_nodes = []
    nodes = self.v1.list_node().items
    for node in self.v1.list_node().items:
      last_condition = node.status.conditions[-1]
      if last_condition.status == "True" and last_condition.type == "Ready" and last_condition.reason == 'KubeletReady':
        ready_nodes.append({
          'name': node.metadata.name,
          'type': 'master' if 'node-role.kubernetes.io/master' in node.metadata.labels else 'worker',
          'capacity': {
            'memory': int(node.status.capacity['memory'][:-2]),
            'cpu': int(node.status.capacity['cpu']) * 1000000000
          }
        })
    return ready_nodes

class Node:

  def __init__(self, node_name):
    config.load_kube_config()
    self.v1 = client.CoreV1Api()
    self.node_name = node_name

  @property
  def metrics(self):
    print('a')
    return self.get_metrics(self.node_name)

  def get_metrics(self, node_name):
    configuration = client.Configuration()
    configuration.api_key_prefix["authorization"] = "Bearer"
    api_client = client.ApiClient(configuration)
    custom_api = client.CustomObjectsApi(api_client)
    response = custom_api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
    print(response)

    #available_nodes = self.get_available_nodes()
    #api_client = client.ApiClient()
    #ret_metrics = api_client.call_api('/apis/metrics.k8s.io/v1beta1/nodes', 'GET', auth_settings=['BearerToken'], response_type='json', _preload_content=False)
    #response = ret_metrics[0].data.decode('utf-8')
    #print(response)    
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
    return available_nodes#

class Pod:

  def __init__(self):
    config.load_kube_config()
    self.v1 = client.CoreV1Api()
    self.metrics = []

  @property
  def metrics(self):
    return []#
