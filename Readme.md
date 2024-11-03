### Introduction
The customer service app , with basic crud operation and SQLLite as data store
API Routes: Defined endpoints
```
CREATE/POST: /customer: Adds a new customer
READ/GET: /customer/<id>: Fetches customer by ID
UPDATE/PUT: /customer/<id>: Updates customer information
DELETE:  /customer/<id>: Deletes customer
```

### Local Development

#### Pre-requisites 
python version =>3.13  with virtual environment

Clone the repository: 

```
git clone git@github.com:madhushesharam/customer-service.git
cd customer-service
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt

```
#### formatter and linter
```
black  app.py  
flake8 app.py   
```

#### unit test and coverage report with pytest and coverage

``` 
pytest test_app.py 
coverage run -m pytest  test_app.py 
coverage report
```

#### run the app in local
```
flask run  
check http://127.0.0.1:5000
```
#### Containarize 
Build the image , using podman just replace podman with docker it should work same

```
podman build -t madhushesharam/customer-service:v1  -f Containerfile  # build and tag 
```
Run the container
podman run -p [host_port]:[container_port] [image_name]

```
podman run -p 8080:5000 localhost/madhushesharam/customer-service:v1  
```
Access service at http://localhost:8080


Tests   (make sure jq is installed)

```
# GET (Home)
curl --request GET --url http://127.0.0.1:8080/

# POST (Create Customer)
customer_response=$(curl --request POST \
  --url http://127.0.0.1:8080/customer \
  --header 'Content-Type: application/json' \
  --data '{
        "firstname": "Madhusaaaaaa",
        "middlename": "NA",
        "lastname": "Shesharam",
        "email": "madhssssu@yaamaaiaail.com",
        "phone": "210-262-2186"
    }')

customer_id=$(echo $customer_response | jq -r .id)


# GET (Retrieve Customer)
curl --request GET \
  --url "http://127.0.0.1:8080/customer/$customer_id" \
  --header 'Content-Type: application/json'

# PUT (Update Customer)
curl --request PUT \
  --url "http://127.0.0.1:8080/customer/$customer_id" \
  --header 'Content-Type: application/json' \
  --data '{
        "firstname": "MadhuCS",
        "lastname": "CSs",
        "email": "madhu@madhu.com",
        "phone": "210-262-2186"
    }'

# DELETE (Delete Customer)
curl --request DELETE \
  --url "http://127.0.0.1:8080/customer/$customer_id/" \
  --header 'Content-Type: application/json'
```

Push container image to docker hub registry
```
podman login docker.io -u madhushesharam -p $password
podman push  madhushesharam/customer-service:v1   # this will be used for k8 deploys.
```

### OpenTelemetry 
Zero-code instrumentation  with the opentelemetry-instrument agent for faster.
https://opentelemetry.io/docs/languages/python/getting-started/#instrumentation

```
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name customer-service \
    flask --app src/app.py run -p 5000
```

### Kubernitize / Kubernetes 
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
#### CI/CD Pipeline Document

Refer -> .github/workflows/main.yml 
Pipeline execution visit-> https://github.com/madhushesharam/customer-service/actions

pipeline for the Python  application. The pipeline automates testing, code quality checks, and deployment to ensure reliable updates to the Kubernetes cluster.(stages/steps have space holders for future code upgrades)


CI 
pipeline runs on  change request to the `main` branch which includes these steps

1. Checkout Code
2. Set Up Python and related dependencies 
3. Install project dependencies from `requirements.txt`.
4. Run Unit Tests  Executes unit tests using `pytest` and checks for at least 70% code coverage
   This is gated, if coverage falls of threshold it exits pipeline. 
5. Code Quality Check
   Format Check 
   Linter Check 
   Automated Quality gates , continues even on failure  
6. Smoke Tests 
  Start the app and perform basic health checks and CRUD operations via API calls.
  TODO: add more detailed tests/frameworks and implement gating  
7. Functional Test
    Runs additional tests using Behave or a similar framework.
    TODO: extend and add more tests , reporting and gating percnetage as required.  
8. Security Scans (Dev Secops)
   Placeholder steps for SCA, secret detection and static analysis , Image Scan etc.
9. Build and Push Docker Image
   If all  steps  pass, builds a  image and pushes it to docker registriy, tagged right


CD (Not Implemented)
TODO
The CD pipeline assumes that a GitOps tool (like ArgoCD or Flux) will deploy the latest Docker image to the Kubernetes cluster after it is pushed to Docker Hub from already onboarded 'customer-deploy-chart/' on gitops tool
  
1. Deployment Trigger: The GitOps tool detects changes and triggers deployment based on Helm charts.
2. Helm Chart Deployment: The application is deployed or updated in the Kubernetes cluster by gitps tool on our behalf

### Assumptions and todo's
- Add authentication jwt etc ..
- The GitOps tool is correctly configured with access to Kubernetes and Docker Hub.
- Helm charts are properly defined in the repository.
- Enahce app to have seprate DataBase managed/onprem cluster
- Enahce helm/k8 deployment to support horizontal scaling
- Define deployment strategy (Blue/Green or Canary) with region based
- Rollback mechanisms are in place for deployments
- Observability for k8 infra and apps in more details with alreting and dashbaords


### Tools/Framework used.
Dev
```
Formatter - https://black.readthedocs.io/en/stable/
linter flake8 https://flake8.pycqa.org
sqlalchemy https://www.sqlalchemy.org/
behave for test - https://behave.readthedocs.io/en/latest/
unit test https://docs.pytest.org
Logger: https://docs.python.org/3/library/logging.html
OpenTelemtry - https://opentelemetry.io/docs/languages/python/getting-started/#instrumentation 
```

Deploy
```
Helm for K8 Manifests - https://helm.sh/docs/helm/helm_create/
Containarization podman alternative to docker - https://podman.io/
kubernetes - k3 https://k3s.io/
```