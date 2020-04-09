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

### Installing

To run the application on a dockerized environment, run:

```
docker-compose build
```

Once build is successful, run:

```
docker-compose up
```

Once it is up, access http://localhost:8888 from your browser, and make sure you receive a HTTP 200 response.

## Acknowledgments

* Thanks to [lindycoder](https://github.com/lindycoder/) whose code has helped in understanding how to initially setup a MySQL container.
