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
        a = True
        #print("error")

def pod_evictor(name, namespace="default"):
    body = client.V1beta1Eviction(metadata=client.V1ObjectMeta(name=name, namespace=namespace))
    try:
        v1.create_namespaced_pod_eviction(name=name, namespace=namespace, body=body)
    except ValueError:
        print("error")

def get_best_node(metrics_items):
	return sorted(metrics_items, key=lambda d: d['memory'])[0]

def get_bad_node(metrics_items):
	higher_node = sorted(metrics_items, key=lambda d: d['memory'], reverse=True)[0]
	return higher_node if int(higher_node['memory']) > 2000000 else {}

def get_target_pods_on_bad_node(bad_node):
    pods = []    
    if len(bad_node) > 0:
        global scheduler_name
        field_selector = 'spec.nodeName='+bad_node['name']+','+'metadata.namespace=lab1'+','+'spec.schedulerName='+scheduler_name
        list = v1.list_pod_for_all_namespaces(watch=False, field_selector=field_selector)

        for item in list.items:
            pod = {}
            pod['name'] = item.metadata.name
            pod['namespace'] = item.metadata.namespace
            pods.append(pod)

    return pods

def get_metrics():
    global best_node
    global bad_node

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
    	new_item['cpu'] = int(item['usage']['cpu'][:-1]) # cpu in nanocores
    	new_item['memory'] = int(item['usage']['memory'][:-2]) # memory in KB
    	metrics_items.append(new_item)

    best_node = get_best_node(metrics_items)
    bad_node = get_bad_node(metrics_items)
    
    print('--------------------------------------------')
    #print(json.dumps(metrics_items, indent=4))
    print("best_node: " + json.dumps(best_node, indent=4))
    print("bad node: " + json.dumps(bad_node, indent=4))

def eviction_workflow():
    get_metrics()
    target_pods_on_bad_node = get_target_pods_on_bad_node(bad_node)
    if len(target_pods_on_bad_node) > 0:
        pod_to_evict = target_pods_on_bad_node[0]
        pod_evictor(pod_to_evict['name'], pod_to_evict['namespace'])

def main():
	# retrieving metrics for the first time
    get_metrics()
    # creating a scheduler to query metrics server every x seconds
    sch = scheduler()
    sch.add_job(eviction_workflow, 'interval', seconds=10)
    sch.start()
    # creating a watch to verify pending pods and binding them to a node
    w = watch.Watch()
    for event in w.stream(v1.list_namespaced_pod, namespace):
        if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name:
            try:
                #print("Scheduling " + event['object'].metadata.name)
                res = pod_scheduler(event['object'].metadata.name, best_node['name'], namespace)
            except client.rest.ApiException as e:
                a = True
                #print(json.loads(e.body)['message'])

if __name__ == '__main__':
    main()


