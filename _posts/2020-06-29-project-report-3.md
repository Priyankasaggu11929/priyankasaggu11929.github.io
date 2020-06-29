---
layout: post
title: "Project Report: Orchestrating a Go application & provisioning a Vagrant box to serve it!"
description: "A project report for orchestrating a Go application using Docker & kubernetes respectively, and provising a vagrant virtual box using Ansible to serve/host it!"
category: Containerization, Docker, Go
tags: [Docker, Containerization, Go, Ansible, Vagrant, Kubernetes]
comments: false
---

June 30, 2020

# Go Application

[Here](https://github.com/Priyankasaggu11929/zerodha-task/tree/master/application) is a sample `Go` application which creates a connection with Redis data structure store. The app increments a `counter`, on every new incoming request & retains the count.

### Setting up the app

- Use `make build` to compile the binary.
- Set the environment variables:
    - `DEMO_APP_ADDR`: Address where the app should listen to
    - `DEMO_REDIS_ADDR`: Address where Redis is running

---

# Problem Description

The project aims to provide a solution for orchestrating the above Go application using the following two container orchestration tools.

1. Docker & Docker-compose
    - Create a `Dockerfile` for the app.
    - Create a `docker-compose.yml` for the app which includes:
        - `redis` service, with the data directory of `redis` mounted at `/data` in your VM.
        - `app` service running with port `8000` exposed to the host.

2. Kubernetes
    - Create a namespace `demo-ops`
    - Create a deployment and service manifest for the app.
    - Configure liveliness check, resource quotas for the deployment.

And then later, provides an *Ansible* playbook for provisiong a *Vagrant* virtual box (or VM) with the following checkpoints.

  - Setup hostname of VM as `demo-ops`.
  - Create a user `demo`.
  - Configure `sysctl` for sane defaults. For eg, increasing open files limit. And finally configure a variety of `sysctl` settings to make the VM a production grade one.
  - Set the system's timezone to "Asia/Kolkata".
  - Install Docker and Docker-Compose.
  - Configure Docker Daemon to have sane defaults. For eg, to keep logs size in check.
  - Deploy the `docker-compose.yml` in `/etc/demo-ops` and start the services

---

# Solution

[***NOTE:*** *The entire solution is present here in this [github repository](https://github.com/Priyankasaggu11929/zerodha-task)!*]


- **STEP 1:** Create a `Dockerfile` for the app.

    ```
    FROM golang:1.12-alpine
    
    # The latest alpine images don't have some tools like (`git` and `bash`).
    # Adding git, bash and openssh to the image
    RUN apk update && apk upgrade && \
        apk add --no-cache bash git openssh
    
    LABEL maintainer="Priyanka Saggu <priyankasaggu11929@gmail.com>"
    
    WORKDIR /app
    
    COPY go.mod go.sum ./
    
    RUN go mod download
    
    COPY . .
    
    RUN go build -o main .
    
    EXPOSE 8080
    
    CMD ["./main"]
    ```

---

- **STEP 2:** Create a `docker-compose.yml` for the app which includes:
    - `redis` service, with the data directory of `redis` mounted at `/data` in your VM.
    - `app` service running with port `8000` exposed to the host.

    ```yaml
    version: '3'
    
    services:
    
      # App Service
      app:
        build:
          context: . 
          dockerfile: Dockerfile
        ports:
          - "8000:8080" 
        restart: unless-stopped
        depends_on:
          - redis 
        environment: 
          DEMO_APP_ADDR: 0.0.0.0:8080
          DEMO_REDIS_ADDR: redis:6379
        networks: 
          - backend
    
      # Redis Service   
      redis:
        image: "redis:alpine" 
        ports:
          - "6379:6379"    
        restart: unless-stopped
        volumes:
          - ./data:/data
        networks:
          - backend
    
    networks:
      backend:
    ```

---

- **STEP 3:** Write a bash script that creates and boots Vagrant box with Ubuntu.

    ```bash
    #!/bin/bash
    
    set -e
    
    ##--- install vagrant if not already setup!---
    
    pkgs='vagrant'
    if ! dpkg -s $pkgs >/dev/null 2>&1; then
        sudo apt install virtualbox
        sudo apt update
        curl -O https://releases.hashicorp.com/vagrant/2.2.6/vagrant_2.2.6_x86_64.deb
        sudo apt install ./vagrant_2.2.6_x86_64.deb
    fi
    
    ##--- verifty vagrant installation---
    
    vagrant --version
    
    mkdir ~/demo-ops
    cd ~/demo-ops
    
    # for a basic Ubuntu 18.04 64-bit Vagrant box
    vagrant init hashicorp/bionic64
    
    vagrant up
    
    # Vagrant IP
    
    IP=$(vagrant ssh -c "ip address show eth0 | grep 'inet ' | sed -e 's/^.*inet //' -e 's/\/.*$//'")
    
    echo "[INFO] Add this IP: $IP under /etc/ansible/hosts for provisioning of the VM through Ansible!"
    
    ##--- SSH into Vagrant VM---
    
    # vagrant ssh
    
    ##--- Halt Vagrant VM---
    
    # vagrant halt
    
    ##--- Halt Vagrant VM---
    
    # vagrant destroy
    ```

***(The vagrant bash script above checks whether Vagrant is already setup on the system or not. If not, It first installs the Vagrant setup, then initializes an Ubuntu Vagrant box, and boots it. It also echos Vagrant VM IP which is supposed to be added under `/etc/ansible/hosts` for provisioning of the VM through Ansible!)***

---

- **STEP 4:** Write ansible playbook(s) to provision the above created Ubuntu Vagrant box with all the checkpoints (memtioned above in the problem description section).

(***NOTE:*** *There are multiple playbooks as a solution here, and all of them are too large to be put here. So, [here](https://github.com/Priyankasaggu11929/zerodha-task/blob/master/playbooks/main.yml) is a github link to all ansible playbooks for the same!*)

### Commands to run the ansible playbook

- *[TODO]* Un-comment this code block [here](https://github.com/Priyankasaggu11929/zerodha-task/blob/master/playbooks/main.yml#L139-L142) and substitute `/home/priyankasaggu119/.ssh/id_rsa.pub` with path to a ssh public-key on your local system.

- Run the following command to provision the VM for the above checkpoints and start the Go services using Docker-compose.

    ```bash
    $ ansible-playbook playbooks/main.yml 
    ```
- Run the following to clean up the docker-compose run.

    ```bash
    $ ansible-playbook playbooks/clean.yml 
    ```

![Ansible_Provisioned_VM](/assets/ansible_run.png)

![Redis_monitoring_requests](/assets/redis-monitor.png)

---

- **STEP 5:** Finally, orchestrate the Go application as kubernetes objects.

    - First, create a redis deployment file & name it `redis-master.yml`.
    
    ```yaml
    ---
    apiVersion: apps/v1 
    kind: Deployment
    metadata:
      name: redis-master 
      labels:
        app: redis      
    spec:
      selector:
        matchLabels:   
          app: redis
          role: master
          tier: backend
      replicas: 1     
      template:      
        metadata:
          labels:   
            app: redis
            role: master
            tier: backend
        spec:      
          containers:
          - name: master
            image: redis
            resources:
              requests:
                cpu: 100m
                memory: 100Mi
            ports:
            - containerPort: 6379
    ---        
    apiVersion: v1
    kind: Service 
    metadata:
      name: redis-master 
      labels:           
        app: redis
        role: master
        tier: backend
    spec:
      ports:
      - port: 6379     
        targetPort: 6379
      selector:       
        app: redis
        role: master
        tier: backend
    ```
        
    - Then create a kubernetes deployment file for the Go application, and name it, `go-redis-app.yml`.
    
    ```yaml
    ---
    apiVersion: apps/v1
    kind: Deployment                 
    metadata:
      name: go-redis-app            
    spec:
      replicas: 2                  
      selector:
        matchLabels:
          app: go-redis-app       
      template:                  
        metadata:
          labels:               
            app: go-redis-app 
        spec:
          containers:
          - name: go-redis-app
            image: priyankasaggu119/go-redis-task:1.0.0 
            imagePullPolicy: IfNotPresent
            resources:
              requests:
                cpu: 100m
                memory: 100Mi
            ports:
              - containerPort: 8080 
            livenessProbe:         
              httpGet:
                path: /
                port: 8080
                scheme: HTTP
              initialDelaySeconds: 5
              periodSeconds: 15
              timeoutSeconds: 5
            readinessProbe:       
              httpGet:
                path: /
                port: 8080
                scheme: HTTP
              initialDelaySeconds: 5
              timeoutSeconds: 1                
            env:                   
              - name: DEMO_APP_ADDR
                value: 0.0.0.0:8080
              - name: DEMO_REDIS_ADDR
                value: redis-master:6379
              - name: REDIS_HOST
                value: redis-master
              - name: REDIS_PORT
                value: "6379"    
    ---
    apiVersion: v1
    kind: Service                 
    metadata:
      name: go-redis-app-service 
    spec:
      type: NodePort            
      ports:                   
      - name: http
        port: 9090
        targetPort: 8080
      selector:
        app: go-redis-app 
    ```

### STEPS TO DEPLOY THE GO/REDIS INCREMENT COUNTER APPLICATION

---

*[**NOTE**: I'm considering here a minikube single node cluster setup!]*

*[Go Application public docker image: [priyankasaggu119/go-redis-task:1.0.0](https://hub.docker.com/layers/priyankasaggu119/go-redis-task/1.0.0/images/sha256-2a8bf9d4a4b037dc579371368fa91bc4476f1979746984050eac76cb491d7953?context=repo)]*

- *STEP 5.1:* Create a namespace `demo-ops`.

```
$ kubectl create namespace demo-ops
```  

- *STEP 5.2:* Deploy Redis (both the kubernetes deployment & service manifest) and check whether the pods are ready & running.

```
$ kubectl apply -f redis-master.yml -n demo-ops

$ kubectl get pods -n demo-ops
```

- *STEP 5.3:* Once the Redis pods are up & running, then deploy the Go application. Once again check whether all the pods are ready.

```
$ kubectl apply -f go-redis-app.yml -n demo-ops

$ kubectl get pods -n demo-ops
```

- *STEP 5.4:* Run the following command to access the go application (exposed via the service). It will output a url.

```
$ minikube service go-redis-app-service --url -n demp-ops
```

- *STEP 5.5:* Hit the endpoint/url (received in the last step).

```
curl <url>
```

![output-screenshot](/assets/output.png)

