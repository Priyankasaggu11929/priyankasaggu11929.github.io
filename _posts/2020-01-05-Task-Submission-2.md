---
layout: post
title: "Project Report - Consul Key-Value Store!"
description: "Documentation for a *Consul Key-Value Store* project."
category: Project
tags: [Project, Consul, DevOps]
comments: false
---

January 05, 2020

# Title: Consul Key-Value Store

# Project Description:

The project aims to provide a REST/CLI solution to access a key-value store. More precisely, it provide a *Get and Set* interface for *getting keys* and *storing data/values* respectively.

# Installation / Usage Instructions:

### Tools/softwares/services used:

- [Consul](https://www.consul.io/)
- [Google Clould Platform (GCP)](https://console.cloud.google.com/)


### Pre-requisites:

- A VM/server for hosting the Consul web UI.

**Note**: *I am using GCP Compute-Engine VM instances for my solution*.

### Steps:

- Create a GCP compute-engine VM instance (in my case, an Ubuntu 18.04 LTS VM, n1-standard-1, 1 vCPU, 3.75 GB memory). Refer [this article](https://www.freecodecamp.org/news/how-to-create-and-connect-to-google-cloud-virtual-machine-with-ssh-81a68b8f74dd/) for the steps to create and connect to a Google Cloud VM via SSH.

- Once you SSH into the VM, the **next step is to setup Consul** (which is an open-source service networking solution to connect and secure services across any runtime platform and public or private cloud). The [official documentation](https://www.consul.io/docs/install/index.html) provides two ways to install Consul:
    1. Using a precompiled binary
    2. Installing from [source](https://www.consul.io/docs/install/index.html#compiling-from-source)

- I will be using the first option for my setup. Here, we are required to download the latest [appropriate package](https://www.consul.io/downloads.html) for our system (which basically is a zip file of pre-compiled binaries. It might require to install `unzip` package in case it is not already available (command: `sudo apt install unzip`)).

```
$ wget "https://releases.hashicorp.com/consul/1.6.2/consul_1.6.2_linux_amd64.zip"

$ unzip consul_1.6.2_linux_amd64.zip
```

- As it is a precompiled binary, the only requirement to have it running is to put the unzipped file in one of our system path setup in our machine.

```
$ echo $PATH

# I will be adding it to the directory path `/usr/local/sbin`. 
# You can add it to any of the path specified in the above output.

$ sudo mv consul /usr/local/sbin
```

- And that is all about the Consul setup/installation. You can verify the installation by running the command `consul` and the output will look like the following.

![Consul-installation](/assets/consul_verify.png)

# Workflow

The workflow for the solution is quite easy and straight-forward. We basically need to do the following:

1. Create a Consul config-file in directory `./consul.d` for ensuruing a smooth access of the Consol web UI.

      ```
      $ mkdir ./consul.d

      $ echo '{
         "client_addr":"0.0.0.0"
      }' > ./consul.d/web.json
      ```

2. Run the Consul Agent, passing the above config-file in the `-config-dir` flag. (Make sure that it keeps running inside one terminal session throughout the rest of the process)

      ```
      $ consul agent -dev -enable-script-checks -config-dir=./consul.d
      ```

      ![Consul-Agent-run-with-config-file-as-flag](/assets/agent-run.png)

3. Inside a new terminal session, use the `Consul kv` command line interface (CLI) to create a new key/value store. We'll use this Consul Key/Value store to add and retrieve key-value pairs. 

      - Below are some of the example commands to demonstrate the process of storing (put) keys and retrieving (get) values from the Consul kv store.

      ```
      # set up a key:value pair <foo:bar> and retrieve the value for key 'foo'.

      $ consul kv put foo bar

      $ consul kv get foo

      # set up another key:value pair <hello:priyankasaggu119> and retrieve the valur for key 'hello'.

      $ consul kv put hello priyankasaggu119

      $ consul kv get hello
      ```

      ![consul-kv-store-demo-cli](/assets/consul_kv_demo.png)

      - To check some additional metadata about the key-value pairs, use the `-detailed` command line flag.

      ```
      $ consul kv get -detailed hello
      ```

      ![consul--key-value-metadata](/assets/detailed-metadata.png)

      - To list all the key-value pairs in a lexicographical order, use the `-recurse` command line flag.

      ```
      $ consul kv get -recurse
      ```

      ![Consul-key-value-pairs-list](/assets/kv-list.png)

      - To modify the value for an existing key, issue the same `consul kv get` command for a key with a new value.

      ```
      # Let's try to modify the value for the key "hello".

      $ consul kv put hello world!
      ```

      ![consul-key-value-modified](/assets/kv-modified.png)
 
      - And finally, to delete a key-value pair from the Consul kv store, use the `delete` command.
 
      ```
      # adding an extra key:value pair <One:1> for demo.

      $ consul kv put One 1

      $ consul kv delete One
      ```

      ![Consul-key-value-delete](/assets/kv-delete.png)

4. With Consul web UI, One can perform all the above operations in a more efficient and easier way.

      - To launch the Consul web UI, access the url, `http://<vm-ipaddress>:8500/ui` in a browser window. (Note: It requires to add a separate firewall rule for exposing port 8500 of the GCP VM. Use this [guide](https://cloud.google.com/vpn/docs/how-to/configuring-firewall-rules) for instructions.)

      ![Consul-Web-UI](/assets/consul-ui.png)

      - Head onto the `Key/Value` section in the navigation bar and you will see all the key-value pairs listed there.

      ![Consul-Web-UI-Key/Value-Pairs](/assets/key-value-pairs.png)

      - All the above Consul CLI operations can be more easily performed using the Consul web UI. From creating a new key-value pair to modifying the existing values, or even deleting the existing key-value pairs, everything can be done from this single UI itself.
   
      ![Consul-create-new](/assets/new.png)

      ![Consul-create-new-key-value-pair](/assets/new-kv.png)

      ![Consul-key-value-store-operations](/assets/operations.png)

      ![Consul-new-key-value-list](/assets/new-list.png)

5. Apart from the local command line Interface (CLI) and the Consul hosted web UI, it is possible to query the Consul key/value store from a remote machine as well using `curl` command.

      ```
      # For example, to get the value and other metadata for key "hello".

      $ curl http://35.223.10.16:8500/v1/kv/hello
      ```

      ![Consul-KV-Store-access-using-curl](/assets/curl-get.png)

      - To add a new key/value pairs from the remote machine, `curl` command will be used with a `PUT` request flag.
 
      ```
      # we are trying to add a new key:value pair <name:priyanka> here.

      $ curl --request PUT --data "priyanka" http://35.223.10.16:8500/v1/kv/name

      true
      ```
    
      ![Curl-Key-value-pair-add](/assets/curl-add-kv.png)

      - Similarly, a key/value pair can be deleted using a `curl` command with `DELETE` request flag.

      ```
      # we are trying to delete the key:value pair with key "name".

      $ curl --request DELETE http://35.223.10.16:8500/v1/kv/name

      true
      ```

      ![Curl-key-value-pair-delete](/assets/curl-delete.png)

# Use Cases, Edge Conditions and Assumptions

The above solution assumes the current setup to be a development environment. Ideally it requires a multi-server Consul setup to achieve a production level, secure environment, which is currently less probable to achieve with the limited amount of computing resources I have.

## Other tools, I tried/re-searched.

- [RabbitMQ](https://www.rabbitmq.com/)
- [GraphQL](https://graphql.org/)

# References

- [KV Store Endpoints](https://www.consul.io/api/kv.html)
- [How to access externally to consul UI](https://stackoverflow.com/questions/35132687/how-to-access-externally-to-consul-ui)
- [Add to Consul KV - Service Configuration](https://learn.hashicorp.com/consul/getting-started/kv)
