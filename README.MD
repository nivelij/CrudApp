# CRUDAPP

Crudapp is a simple python-based web application that can perform CRUD operation, that's it, literally. The idea is not to create a simple web application, because where's the fun right? The idea is to use this app as a playground for containerization, and to help beginners in understanding how containerization and orchestration is being implemented in real application.

## Getting Started

Clone this project to your machine. If you want to run this project in a VM, make sure you have your virtualization software installed. I developed this repository on Oracle VirtualBox 6.1.2

### Prerequisites

Make sure you have ```docker``` and ```docker-compose``` installed on your machine.

1. Install ```docker```:
```
# Setting up docker repository
$ sudo apt-get update
$ sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo apt-key fingerprint 0EBFCD88
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Install docker
$ sudo apt-get update
$ sudo apt-get install docker-ce

# Verify that docker is installed
$ docker --version
```

2. Install ```docker-compose```:
```
$ sudo curl -L "https://github.com/docker/compose/releases/download/<LATEST_DOCKER_VERSION>/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose

# Verify that docker-compose is installed
$ docker-compose --version
```

### Installing and Deploying the Stack Locally

To run the application on a dockerized environment, run:

```
docker-compose build
```

Once build is successful, run:

```
docker-compose up
```

Once it is up, access http://localhost from your browser, and make sure you receive a HTTP 200 response.

### Deploying the Stack on Docker Swarm

In order for the stack to be deployable on swarm, the image needs to be available in docker registry, be it locally or on docker hub. In this example, I pushed those images to docker hub.
Another thing to note is that there is a need to have a manager machine (where docker swarm deployment is being managed) as well as swarm node machine (where manager can assign particular container to run on the machine. If you want to follow this setup, I strongly recommend to provision different virtual machines and install docker there.

#### Setting up Docker Manager

Initiate docker swarm and make the current machine as docker manager:

```
$ docker swarm init --advertise-addr <DOCKER_MANAGER_MACHINE_IP_ADDRESS>
Swarm initialized: current node (bvz81updecsj6wjz393c09vti) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-1awxwuwd3z9j1z3puu7rcgdbx 172.17.0.2:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
``` 

Pay attention to ```docker swarm join ...``` command printed above. We need this command to be executed in the swarm node machine so that it can join the node

#### Setting up Swarm Node as Worker

Run the ```docker swarm join ...``` command

```
docker swarm join --token SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-1awxwuwd3z9j1z3puu7rcgdbx 172.17.0.2:2377
This node joined a swarm as a worker.
```

#### Deployment

Before deploying the stack, go back to docker manager node and run this command to check if the worker node has been connected successfully:

```
$ docker node ls

ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS      ENGINE VERSION
6iz7q2kmrsufbiyg0v9qept47     Worker              Ready               Active                                  19.03.8
qhi2313bxiayfoxbixu9kjs2t *   krisha-VirtualBox   Ready               Active              Leader              19.03.8
```

If you see this, then your docker swarm setup is good and we are ready to deploy the stack. To deploy the stack, run:

```
$ docker stack deploy --compose-file=docker-compose.yml crudapp

Creating network crudapp_default
Creating service crudapp_api
Creating service crudapp_db
Creating service crudapp_nginx
```

Once done, run this command to verify the service is running:

```
$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE                          PORTS
35yndc8c9k1h        crudapp_api         replicated          1/1                 nivelij/crudapp_api:latest     
qc2d3a9cuhz6        crudapp_db          replicated          1/1                 nivelij/crudapp_db:latest      
hi9ti7t67myu        crudapp_nginx       replicated          1/1                 nivelij/crudapp_nginx:latest   *:80->80/tcp
```

You can also run ```docker stats``` or ```docker ps``` command to see how the containers are distributedly deployed:

In manager node:

```
$ docker stats

CONTAINER ID        IMAGE                                COMMAND                  CREATED             STATUS              PORTS                                                                           NAMES
a44a5f27a5a1        nivelij/crudapp_db:latest            "docker-entrypoint.s…"   2 minutes ago       Up 2 minutes        3306/tcp                                                                        crudapp_db.1.i96v9zehm69cifmemw9vx8yie
```

In worker node:

```
$ docker stats

CONTAINER ID        IMAGE                                COMMAND                  CREATED             STATUS              PORTS                                                                           NAMES
b2e04dbbe0c3        nivelij/crudapp_nginx:latest         "nginx -g 'daemon of…"   16 seconds ago      Up 10 seconds       80/tcp                                                                          crudapp_nginx.1.xy09awqmr0q3vpl6dvvzuqfj3
acc192a61c07        nivelij/crudapp_api:latest           "python main.py"         25 seconds ago      Up 17 seconds                                                                                       crudapp_api.1.hzwxgwum18a7fa8myrajsflts
```

You can also scale the sevice as you please. Run this command ```docker service scale <SERVICE_NAME>=<SIZE>```

```
$ docker service scale crudapp_api=3

crudapp_api scaled to 3
overall progress: 3 out of 3 tasks 
1/3: running   [==================================================>] 
2/3: running   [==================================================>] 
3/3: running   [==================================================>] 
verify: Service converged 
```

Now run ```docker service ls``` and see the latest scale:

```
$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE                          PORTS
35yndc8c9k1h        crudapp_api         replicated          3/3                 nivelij/crudapp_api:latest     
qc2d3a9cuhz6        crudapp_db          replicated          1/1                 nivelij/crudapp_db:latest      
hi9ti7t67myu        crudapp_nginx       replicated          1/1                 nivelij/crudapp_nginx:latest   *:80->80/tcp
```

If you are new to performance scalability, it is now the best time to load up the JMeter project included in this repository, use different size of thread and total requests, and see how the application perform under different kind of load.
Docker makes it so easy to scale the running service, so feel free to scale up or scale down as you please, and observe the increase or decrease in overal performance.


## Acknowledgments

* Thanks to [lindycoder](https://github.com/lindycoder/) whose code has helped in understanding how to initially setup a MySQL container.
