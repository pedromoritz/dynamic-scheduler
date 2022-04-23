#!/usr/bin/env python

import time
import random
import json

from kubernetes import client, config, watch
from apscheduler.schedulers.background import BackgroundScheduler as scheduler

config.load_kube_config()
v1 = client.CoreV1Api()
sysdig_metric = "net.http.request.time"
metrics = [{ "id": sysdig_metric, "aggregations": { "time": "timeAvg", "group": "avg" } }]

scheduler_name = "ppgcc_scheduler"
namespace = "lab1"
best_node_memory = None

def get_request_time(hostname):
    hostfilter = "host.hostName = '%s'" % hostname
    start = -60
    end = 0
    sampling = 60
    metricdata = sdclient.get_data(metrics, start, end, sampling, filter=hostfilter)
    request_time = float(metricdata[1].get('data')[0].get('d')[0])
    print(hostname + " (" + sysdig_metric + "): " + str(request_time))
    return request_time

def best_request_time(nodes):
    if not nodes:
        return []
    node_times = [get_request_time(hostname) for hostname in nodes]
    best_node = nodes[node_times.index(min(node_times))]
    print("Best node: " + best_node)
    return best_node

def best_memory_node(nodes):
    if not nodes:
        return []
    node_times = [get_request_time(hostname) for hostname in nodes]
    best_node = nodes[node_times.index(min(node_times))]
    print("Best node: " + best_node)
    return best_node

def nodes_available():
    ready_nodes = []
    for n in v1.list_node().items:
        for status in n.status.conditions:
            if status.status == "True" and status.type == "Ready":
                ready_nodes.append(n.metadata.name)
    return ready_nodes

def pod_scheduler(name, node, namespace="default"):
    target = client.V1ObjectReference(kind = 'Node', api_version = 'v1', name = node)
    meta = client.V1ObjectMeta(name = name)
    body = client.V1Binding(target = target, metadata = meta)
    try:
        client.CoreV1Api().create_namespaced_binding(namespace=namespace, body=body)
    except ValueError:
        print("error")

def request_nodes():
    api_client = client.ApiClient()
    ret_metrics = api_client.call_api('/apis/metrics.k8s.io/v1beta1/nodes', 'GET', auth_settings=['BearerToken'], response_type='json', _preload_content=False)
    response = ret_metrics[0].data.decode('utf-8')
    response_obj = json.loads(response)
    print(json.dumps(response_obj["items"], indent=4))

def main():
    sch = scheduler()
    sch.add_job(request_nodes, 'interval', seconds=5)
    sch.start()
    w = watch.Watch()
    for event in w.stream(v1.list_namespaced_pod, namespace):
        if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name:
            try:
                print("Scheduling " + event['object'].metadata.name)
                res = pod_scheduler(event['object'].metadata.name, 'ppgcc-m04', namespace)
            except client.rest.ApiException as e:
                print(json.loads(e.body)['message'])


if __name__ == '__main__':
    main()                                                                                                                                                                  


