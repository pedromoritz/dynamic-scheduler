#!/usr/bin/env python

import time
import random
import json

from kubernetes import client, config, watch
from apscheduler.schedulers.background import BackgroundScheduler as scheduler

config.load_kube_config()
v1 = client.CoreV1Api()

scheduler_name = "ppgcc_balancer"
namespace = "lab1"
best_node = {}
bad_node = {}

def nodes_available():
    ready_nodes = []
    nodes = v1.list_node().items
    print(nodes)

    #for n in v1.list_node().items:
    #    for status in n.status.conditions:
    #        if status.status == "True" and status.type == "Ready":
    #            ready_nodes.append(n.metadata.name)
    #return ready_nodes

def pod_scheduler(name, node, namespace="default"):
    target = client.V1ObjectReference(kind = 'Node', api_version = 'v1', name = node)
    meta = client.V1ObjectMeta(name = name)
    body = client.V1Binding(target = target, metadata = meta)
    try:
        client.CoreV1Api().create_namespaced_binding(namespace=namespace, body=body)
    except ValueError:
        print("error")

def get_best_node(metrics_items):
	return sorted(metrics_items, key=lambda d: d['memory'])[0]

def get_bad_node(metrics_items):
	higher_node = sorted(metrics_items, key=lambda d: d['memory'], reverse=True)[0]
	return higher_node if int(higher_node['memory']) > 2000000 else {}

def find_target_pods_on_bad_node(bad_node):
	return [] #sorted(metrics_items, key=lambda d: d['memory'], reverse=True)[0]

def get_metrics():
    global best_node
    api_client = client.ApiClient()
    ret_metrics = api_client.call_api('/apis/metrics.k8s.io/v1beta1/nodes', 'GET', auth_settings=['BearerToken'], response_type='json', _preload_content=False)
    response = ret_metrics[0].data.decode('utf-8')
    response_obj = json.loads(response)
    metrics_items_raw = response_obj["items"]

    metrics_items = []
    for item in metrics_items_raw:
    	new_item = {}
    	new_item['name'] = item['metadata']['name']
    	new_item['timestamp'] = item['timestamp']
    	new_item['cpu'] = item['usage']['cpu'][:-1] # cpu in nanocores
    	new_item['memory'] = item['usage']['memory'][:-2] # memory in KB
    	metrics_items.append(new_item)

    best_node = get_best_node(metrics_items)
    bad_node = get_bad_node(metrics_items)
    #find_target_pods_on_bad_node(bad_node)
    print("best_node: " + json.dumps(best_node, indent=4))
    print("bad node: " + json.dumps(bad_node, indent=4))

def main():
	# retrieving metrics for the first time
    get_metrics()
    print(best_node)
    # creating a scheduler to query metrics server every x seconds
    sch = scheduler()
    sch.add_job(get_metrics, 'interval', seconds=10)
    sch.start()
    # creating a watch to verify pending pods and binding them to a node
    w = watch.Watch()
    for event in w.stream(v1.list_namespaced_pod, namespace):
        if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name:
            print(event['object'].metadata.name)
            try:
                print("Scheduling " + event['object'].metadata.name)
                res = pod_scheduler(event['object'].metadata.name, best_node['name'], namespace)
            except client.rest.ApiException as e:
                print(json.loads(e.body)['message'])

if __name__ == '__main__':
    main()

# analisa se ha target pod a ser movido
# seleciona se ha no com melhor quantidade de recursos
# gera a eviction do pod
#testar 
#podName = 'insert-name-of-pod'
#podNamespace = 'insert-namespace-of-pod'
#body = client.V1beta1Eviction(metadata=client.V1ObjectMeta(name=podName, namespace=podNamespace))
#api_response = v1.create_namespaced_pod_eviction(name=podName, namespace=podNamespace, body=body)

# faz o schedule para o no destino


