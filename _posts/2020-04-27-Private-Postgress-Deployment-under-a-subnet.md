---
layout: post
title: "Custom GCP type provider for automating `VPC Network Peering` creation!"
description: "Writing custom GCP type provider for VPC Network Peering, thus to deploy a private Postgres Cloud SQL instance through deployment manager."
category: Writing
tags: [GCP, GCP-Type-Providers, Postgres, Cloud-SQL, Cloud, Deployment-manager, VPC-Network-Peering]
comments: false
---

April 26, 2020

Yesterday, I wrote a post around [writing custom GCP type providers](https://priyankasaggu11929.github.io/writing/2020/04/26/Custom-GCP-TypeProviders.html). 

That post basically provided a solution to one of the problems I faced while deploying a resource (*a private dataproc cluster with a Presto installation on it*) on GCP for which there was no official GCP type provider available.

Today's post is just an extension with a similar use-case where again, I needed to write a custom GCP type provider, to solve the issue.

---

## Problem Statement:

**Manual Steps**

- I was trying to create a private `Postgres Cloud SQL instance`.

- From GCP UI, when I try to choose Private IP and then select a network VPC. There, in turn, appears a button named `Allocate and connect`.

![postgres-on-UI](/assets/postgres.png)

- This `Allocate and connect` button when clicked, automatically creates the `VPC Network Peering` for the respective VPC network (under which I want to deploy the required instance).

![VPC-network-peering](/assets/peering.png)

**Actual problem**

- Now, on the contrary, when I tried to deploy private `Postgres Cloud SQL instance` using a jinja template (from deployment-manager), it doesn't create this `VPC Network Peering` dynamically/automatically. 

So, the use-case here is ***to achieve this automatic `VPC Network Peering` creation through the DM templates.***

Or better I say, I wanted the outcome from the command below, to be achieved directly through the deployment manager(DM) templates.

```
gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --ranges=<my-range> --network=<my-network> --project=<my-project>
```
---

This time, I will go on the solution part directly. 

***Here is the link to [the issue](https://github.com/GoogleCloudPlatform/deploymentmanager-samples/issues/549) I raised, that covers *all* the small bits & discussion around how we finally managed to reach at the desired solution.***

---

## Solution:

***Note: The solution below includes the entire process of creating:
1. A VPC Network
2. Network Subnets
3. VPC Network Peering (achieved by custom type-provider)
4. Google Managed Services
5. Postgres Cloud-SQL instance with a database & root user***

- **Step1:** Create an `options.yaml` file with the following contents:

```yaml
options:
    inputMappings:
        - fieldName: Authorization
          location: HEADER
          value: $.concat("Bearer ", $.googleOauth2AccessToken())
          methodMatch: .*
```

- **Step2:** Create the custom GCP type provider with the following command (where `vpcpeering-v1beta-type` is the name of the custom GCP type provider):

```
gcloud beta deployment-manager type-providers create vpcpeering-v1beta-type --descriptor-url='https://servicenetworking.googleapis.com/$discovery/rest?version=v1' --api-options-file options.yaml
```
- **Step3:** Create a jinja template file `example-postgres.jinja` with the following contents:

```yaml
{ % set ID = env['name'] %}

resources:

######## Network ###########

- name: { { ID }}-network
  type: compute.v1.network
  properties:
    autoCreateSubnetworks: false

######### SUBNETS ##########

{ % for i in range(properties["ipCidrRange"]|length) %}
- name: { { ID }}-subnet-{{ i }}
  type: compute.v1.subnetwork
  properties:
    network: $(ref.{ { ID }}-network.selfLink)
    privateIpGoogleAccess: true
    ipCidrRange: { { properties["ipCidrRange"][i] }}
    region: { { properties["region"] }}
    logConfig:
      aggregationInterval: { { properties["log"]["aggregationInterval"] }}
      flowSampling: { { properties["log"]["flowSampling"] }}
      enable: true
{ % endfor %}

######### VPC NETWORK PEERING ##########

- name: addpeering
  action: {project-id}/vpcpeering-v1beta-type:servicenetworking.services.connections.create
  properties:
    parent: services/servicenetworking.googleapis.com
    network: projects/{project-id}/global/networks/{ { ID }}-network
    peering: cloudsql-postgres-googleapis-com
    reservedPeeringRanges:
    - google-managed-services-{ { ID }}-network
  metadata:
    dependsOn:
    - { { ID }}-network

######### GOOGLE MANAGED SERVICES ##########

- name: google-managed-services-{ { ID }}-network
  type: compute.beta.globalAddress
  properties:
    network: $(ref.{ { ID }}-network.selfLink)
    purpose: VPC_PEERING
    addressType: INTERNAL
    prefixLength: 16

# ########## POSTGRES CREATION ##########
  
- name: { { ID }}-master
  type: gcp-types/sqladmin-v1beta4:instances
  properties:
    region: { { properties['region'] }}  
    backendType: { { properties['backendType'] }}  
    gceZone: { { properties['gceZone'] }}  
    instanceType: CLOUD_SQL_INSTANCE
    databaseVersion: { { properties['databaseVersion'] }}  
    settings:
      tier: { { properties['ptier'] }}
      activationPolicy: ALWAYS
      availabilityType: ZONAL
      backupConfiguration:
        enabled: true
        pointInTimeRecoveryEnabled: false
        replicationLogArchivingEnabled: false
      dataDiskSizeGb: { { properties['dataDiskSizeGb'] }}
      dataDiskType: { { properties['dataDiskType'] }}      
      ipConfiguration:
        authorizedNetworks:
        - kind: sql#aclEntry
          name: { { properties["ipConfiguration"]["authorizedNetworks"]["name"] }}
          value: { { properties["ipConfiguration"]["authorizedNetworks"]["value"] }}
        ipv4Enabled: true
        privateNetwork: projects/{project-id}/global/networks/{ { ID }}-network
  metadata:
    dependsOn:
    - { { ID }}-network
    - addpeering

- name: { { ID }}-db
  type: gcp-types/sqladmin-v1beta4:databases
  properties:
    name: { { properties["database"]["name"] }}
    instance: $(ref.{ { ID }}-master.name)
    charset: { { properties["database"]["charset"] }}

- name: { { ID }}-db-root
  type: gcp-types/sqladmin-v1beta4:users
  properties:
    name: { { properties["database-root"]["user"] }}
    instance: $(ref.{ { ID }}-master.name)
    host: ""
    password: { { properties["database-root"]["password"] }}
  metadata:
    dependsOn:
    - { { ID }}-db
```

- **Step4:** Create the `config.yaml` file (for testing) with the contents below:

```yaml
imports:
- path: example-postgres.jinja

resources:

- name: demo
  type: example-postgres.jinja
  properties:
    region: us-west1
    zone: us-west1-a

###### VPC CONFIGS ###### 

    ipCidrRange:
    - 172.16.0.0/21
    log:
      aggregationInterval: INTERVAL_10_MIN
      flowSampling: 0.5

###### POSTGRES CONFIGS ######

    backendType: SECOND_GEN
    gceZone: us-west1-a
    databaseVersion: POSTGRES_11
    ptier: db-custom-2-7680
    dataDiskSizeGb: '10'
    dataDiskType: PD_SSD
    ipConfiguration:
      authorizedNetworks:
        name: example
        value: {ip-range}
    database:
      name: test
      charset: utf8
    database-root:
      user: root
      password: password 
```

You may want to change the following values too:

1. `project-id`
2. Inside config.yaml,
    - change `name` & `value` in `ipConfiguration` -> `authorizedNetworks`.
    - And pass `user` and `password` values accordingly in `database-root` section.

Finally, if everything happens the intended way, You will have a private **`Postgres Cloud SQL instance`** along with a successful automatic **`VPC Network Peering`** connection.

That's all for this time. \o/

### REFERENCES:

- [1] Github thread: (Private VPC Peering for Cloud SQL is not supported by deployment manager #549)[https://github.com/GoogleCloudPlatform/deploymentmanager-samples/issues/549]
- [2] Discovery Document: [https://servicenetworking.googleapis.com/$discovery/rest?version=v1](https://servicenetworking.googleapis.com/$discovery/rest?version=v1)
- [3] [Service Network API](https://cloud.google.com/service-infrastructure/docs/service-networking/reference/rest)


