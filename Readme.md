### Introduction

### Local Development

Clone the repository: <URL>

### Pre-requisites
Set up a virtual environment on Mac

```
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```
### formatter and linter
```
black  app.py  
flake8 app.py   

```

### unit test and coverage report with pytest and coverage

``` 
pytest test_app.py 
coverage run -m pytest  test_app.py 
coverage report
```
### run the app in local
```
flask run  # http://127.0.0.1:5000

```
#### Containarize 
Build the image , using podman just replace podman with docker it should work same

```
podman build -t madhushesharam/customer-service:v1  -f Containerfile  # build and tag 
```
Run the container
podman run -p [host_port]:[container_port] [image_name]

```
podman run -p 8080:5000 localhost/customer-service:latest 

```
Access service at http://localhost:8080

```
podman login docker.io -u madhushesharam -p $password
podman push  madhushesharam/customer-service:v1   # this will be used for k8 deploys.
```

#### Kubernitize
Create k8 deployment for app using helm

#### pre-requisites/assumptions 
helm and k3's/MiniKube/Kind/K8Cluster is made available  
Will be using k3's here https://docs.k3s.io/

```
helm create customer-deploy-chart 
# post helm template  creation , update image ref and service type to be load balancer.
cd customer-deploy-chart 

Point to Cluster /Auth
kubectl create ns dev  && kubectl config set-context --current --namespace=dev 
helm install customer-service -f values.yaml .  |  helm upgrade customer-service -f values.yaml . 

kubectl get deployment
NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE
customer-service-customer-deploy-chart   1/1     1            1           66s

```
Get the service URL for validation and tests.
```
kubectl get svc customer-service-customer-deploy-chart -o yaml | yq .status
{
  "loadBalancer": {
    "ingress": [
      {
        "ip": "192.168.64.4",
        "ipMode": "VIP"
      }
    ]
  }
}
```

Test the deployment
```
curl -i http://192.168.64.4:5000/   

HTTP/1.1 200 OK
Server: Werkzeug/3.1.1 Python/3.13.0
Date: Sat, 02 Nov 2024 20:33:59 GMT
Content-Type: application/json
Content-Length: 42
Connection: close

{"message":"welcome to customer service"}
```