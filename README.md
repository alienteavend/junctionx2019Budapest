# TESCO NomNom - PI-rates junctionX 2019
![logo](https://i.ibb.co/nf4DxdT/tesconomnom-logo.png "TESCO NomNom")

## About the project
During Junction X Budapest 2019, our team decided to work on TESCO's proposed problem: reducing food waste.

Our solution is based on a fair draft between charities and third parties who are willing to take away food that would be thrown away.

Read more about the challenge here:
https://budapest.hackjunction.com/challenges/tesco-technology

### User journey
![user_journey](https://ibb.co/ypx3y7Q "User Journey")
https://ibb.co/ypx3y7Q

### UI design plans
https://www.figma.com/proto/U8dXC8Tlt5rSI22u0PptV7/Junction?node-id=100%3A17235&scaling=min-zoom

### Mind maps created during the project
https://coggle.it/diagram/XbR3MybMqum4peZu/t/nomnom (hungarian)

## For developers
We implemented the draft system during the hackathon.

The solution we created is a Python flask backend with vue frontend. You can see the following instructions to set up a scaleable docker swarm or kubernetes cluster with our dockers.
### Docker

Build the images and spin up the containers:

```sh
$ docker-compose up -d --build
```

Run the migrations and seed the database:

```sh
$ docker-compose exec server python manage.py recreate_db
$ docker-compose exec server python manage.py seed_db
```

Test it out at:

1. [http://localhost:8080/](http://localhost:8080/)
1. [http://localhost:5001/drafts/ping](http://localhost:5001/books/ping)
1. [http://localhost:5001/books](http://localhost:5001/books)

### Kubernetes

#### Minikube

Install and run [Minikube](https://kubernetes.io/docs/setup/minikube/):

1. Install a  [Hypervisor](https://kubernetes.io/docs/tasks/tools/install-minikube/#install-a-hypervisor) (like [VirtualBox](https://www.virtualbox.org/wiki/Downloads) or [HyperKit](https://github.com/moby/hyperkit)) to manage virtual machines
1. Install and Set Up [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to deploy and manage apps on Kubernetes
1. Install [Minikube](https://github.com/kubernetes/minikube/releases)

Start the cluster:

```sh
$ minikube start --vm-driver=virtualbox
$ minikube dashboard
```

#### Volume

Create the volume:

```sh
$ kubectl apply -f ./kubernetes/persistent-volume.yml
```

Create the volume claim:

```sh
$ kubectl apply -f ./kubernetes/persistent-volume-claim.yml
```

#### Secrets

Create the secret object:

```sh
$ kubectl apply -f ./kubernetes/secret.yml
```

#### Postgres

Create deployment:

```sh
$ kubectl create -f ./kubernetes/postgres-deployment.yml
```

Create the service:

```sh
$ kubectl create -f ./kubernetes/postgres-service.yml
```

Create the database:

```sh
$ kubectl get pods
$ kubectl exec postgres-<POD_IDENTIFIER> --stdin --tty -- createdb -U postgres drafts
```

#### Flask

Build and push the image to Docker Hub:

```sh
$ docker build -t junctionxpirates/tesco-nomnom-flask ./services/server
$ docker push junctionxpirates/tesco-nomnom-flask
```

> Make sure to replace `junctionxpirates` with your Docker Hub namespace in the above commands as well as in *kubernetes/flask-deployment.yml*

Create the deployment:

```sh
$ kubectl create -f ./kubernetes/flask-deployment.yml
```

Create the service:

```sh
$ kubectl create -f ./kubernetes/flask-service.yml
```

Apply the migrations and seed the database:

```sh
$ kubectl get pods
$ kubectl exec flask-<POD_IDENTIFIER> --stdin --tty -- python manage.py recreate_db
$ kubectl exec flask-<POD_IDENTIFIER> --stdin --tty -- python manage.py seed_db
```

#### Ingress

Enable and apply:

```sh
$ minikube addons enable ingress
$ kubectl apply -f ./kubernetes/minikube-ingress.yml
```

Add entry to */etc/hosts* file:

```
<MINIKUBE_IP> hello.world
```

Try it out:

1. [http://hello.world/drafts/info](http://hello.world/drafts/info)


#### Vue

Build and push the image to Docker Hub:

```sh
$ docker build -t junctionxpirates/tesco-nomnom-vue ./services/client \
    -f ./services/client/Dockerfile-minikube
$ docker push junctionxpirates/tesco-nomnom-vue
```

> Again, replace `junctionxpirates` with your Docker Hub namespace in the above commands as well as in *kubernetes/vue-deployment.yml*

Create the deployment:

```sh
$ kubectl create -f ./kubernetes/vue-deployment.yml
```

Create the service:

```sh
$ kubectl create -f ./kubernetes/vue-service.yml
```

Try it out at [http://hello.world/](http://hello.world/).
