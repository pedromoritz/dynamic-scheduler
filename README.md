## Dynamic Scheduler

### Criar cluster Kubernetes
minikube start --nodes 4 -p ppgcc --cpus 2 --memory 4096 --vm --kubernetes-version=v1.24.3
minikube start --nodes 3 -p ppgcc --cpus 2 --memory 1900 --vm --kubernetes-version=v1.24.3

### Habilitar metrics API
minikube addons enable metrics-server -p ppgcc

### Criar namespace lab
kubectl create namespace lab

### Remover deployments do namespace lab
kubectl --namespace lab delete deployments `kubectl get deployments --namespace lab --no-headers -o custom-columns=":metadata.name"`

### Remover pods do namespace lab
kubectl --namespace lab delete pod `kubectl get pods --namespace lab1 --no-headers -o custom-columns=":metadata.name"`

COMANDOS ÚTEIS

LISTAR SERVIÇOS
minikube service list -p ppgcc

LISTAR INFO DOS PODS DO NAMESPACE LAB1
kubectl get pods --namespace lab1 -o wide

EXIBIR RECURSOS DOS PODS DO NAMESPACE LAB1
kubectl top node --namespace lab1

MOSTRAR DASHBOARD
minikube dashboard -p ppgcc

EXIBIR NODES VIA METRICS API
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes

REMOVER PODS DO NAMESPACE LAB1
kubectl --namespace lab1 delete pod `kubectl get pods --namespace lab1 --no-headers -o custom-columns=":metadata.name"

EXIBIR LOG DO TEST POD
kubectl --namespace lab1 logs -f `kubectl get pods --namespace lab1 --no-headers -o custom-columns=":metadata.name" |grep scheduler`

#### Para gerar os diagramas de classes e pacotes
sudo apt install pylint graphviz
pyreverse -o png .
