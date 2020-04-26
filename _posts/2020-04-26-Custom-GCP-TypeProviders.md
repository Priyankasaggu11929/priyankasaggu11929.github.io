---
layout: post
title: "Automating private dataproc cluster deployment having Presto Installation (on GCP)!"
description: "Writing custom type-providers for PRESTO installation on DataProc Cluster."
category: Writing
tags: [GCP, GCP-Type-Providers, PRESTO, DataProc, Cloud, Deployment-manager]
comments: false
---

April 26, 2020

A few weeks back, I was working on writing automation templates, for achieving a *one click deployment* of the entire [Atlan](https://atlan.com) stack, on Google Cloud Platform(GCP).

Here, the good part is that GCP has its own internal tool/software, called [deployment-manager](https://cloud.google.com/deployment-manager), for writing Infrastructure-as-Code(IaC). It supports automation using Jinja & Python templates.

I chose to write all my templates using Jinja. Because Jinja templates are far more readable in this case (in comparision to Python templates). These are (almost) similar to JSON configuration description of the resource (to be deployed).

Okay, I think this was a quick good intro to what I was trying to achieve that time. But this post actually focuses more on providing a solution to one of the problems, I faced during the time.

---

## Problem Statement:

During the process, it required me to deploy a private dataproc cluster having a Presto installation on it. Doing it from the GCP UI, was pretty straight forward. But, (as per my use-case) I was to write a Jinja template to achieve this *private dataproc cluster with Presto installation* deployment using deployment-manager. And this was not happening for me, the intended way.

I was able to deploy a private dataproc cluster, but was not able to achieve the Presto installation part on it.

## Approach:

The jinja template I wrote for the above use-case, looked like this:

```yaml
resources:
- name: Dataproc-cluster
  type: gcp-types/dataproc-v1:projects.regions.clusters
  properties:
    region: { { properties["region"] }}
    projectId: { { env["project"]|safe }}
    clusterName: { { clusterName|safe }}
    config:
      configBucket: example-bucket
      gceClusterConfig:
        zoneUri: https://www.googleapis.com/compute/v1/projects/{ { env["project"]|safe }}/zones/{ { properties["zone"]|safe }}
        tags: 
        - example-firewall-rule
        subnetworkUri: https://www.googleapis.com/compute/v1/projects/{ { env["project"]|safe }}/regions/{ { properties["zone"]|safe }}/subnetworks/example-subnet-1
        internalIpOnly: true
      masterConfig:
        numInstances: 1
        machineTypeUri: https://www.googleapis.com/compute/v1/projects/{ { env["project"]|safe }}/zones/{ { properties["zone"]|safe }}/machineTypes/n1-standard-2
        diskConfig:
          bootDiskSizeGb: 200
          bootDiskType: pd-ssd
      workerConfig:
        numInstances: 2
        machineTypeUri: https://www.googleapis.com/compute/v1/projects/{ { env["project"]|safe }}/zones/{ { properties["zone"]|safe }}/machineTypes/n1-standard-2
        diskConfig: 
          bootDiskSizeGb: 200
          bootDiskType: pd-ssd
      softwareConfig:
        imageVersion: 1.4.23-ubuntu18
        optionalComponents: 
        - PRESTO
```

If you see the third line above, I have used a `type: gcp-types/dataproc-v1:projects.regions.clusters` field under the `resources:` section. 

The value of this `type:` field is generally what is known as a ***GCP type provider***. 

> A type provider exposes all resources of a third-party API to Deployment Manager as base types that you can use in your configurations. These types must be directly served by a RESTful API that supports Create, Read, Update, and Delete (CRUD)
>
> - *[Documentation - Google Cloud Platform](https://cloud.google.com/deployment-manager/docs/configuration/type-providers/creating-type-provider)*

I'm quite sure that the definition above doesn't make much sense in the first go itself. So, just to break it down for you, I will say this GCP type provider, when used/mentioned inside a jinja template (or a python template), instructs the deployment manager to create/deploy/instantiate a GCP computing resource. Besides, it sets the configuration of that resource as defined by the later part of the template.

For instance, 

- `gcp-types/compute-v1` type provider instantiates a coumpute engine (VM instance).
- `gcp-types/storage-v1` type provider instantiates a GCS storage bucket.
- `cp-types/container-v1` type provider instantiates a Kubernetes cluster (GKE), etc.

The whole list of supported GCP type providers is present [here](https://cloud.google.com/deployment-manager/docs/configuration/supported-gcp-types).

(*Hope that makes some sense now*)

Now, in our case, `type: gcp-types/dataproc-v1:projects.regions.clusters` instructs the deployment manager to deploy a dataproc cluster with a master & 2 worker nodes.

If you see the last 2 lines of the above template, it also instructs to install `PRESTO` as an optional component on the cluster.

And that is where our above template doesn't work the intended way. Ideally, it should install the `PRESTO` as an optional component on the dataproc cluster. But the deployment manager is not able to achieve that using our specified GCP type provider.

## What was the problem?

After doing endless research on it, I had no option left but to finally raise it as an issue on the [deploymentmanager-samples Github repository](https://github.com/GoogleCloudPlatform/deploymentmanager-samples/issues/546).

And there, [Adam Ocsvari(ocsig)](https://github.com/ocsig) nicely explained and pointed it out:

> The Google Analytics(GA) API does NOT support PRESTO, but only the BETA API does. But unfortunately, there is no any official GCP type provider released for `dataproc-v1beta`.
> So, the final solution comes out to be writing a custom GCP type provider to achieve the same.

---

## Solution:

So, here is the final solution, which involves writing a custom GCP type provider. 

The steps goes like the following:

- **Step1**: Create an `options` file, say `dataproc-v1beta.type.yaml` and paste the following contents in there.


```
options:
    inputMappings:
        - fieldName: Authorization
          location: HEADER
          value: $.concat("Bearer ", $.googleOauth2AccessToken())
          methodMatch: .*
    collectionOverrides:
    - collection: projects.regions.clusters
      options:
        virtualProperties: |
          schema: http://json-schema.org/draft-04/schema#
          type: object
          properties:
            region:
              type: string
          required:
          - region
        inputMappings:
        - methodMatch: ^(create|update|get|patch|delete)$
          location: PATH
          fieldName: region
          value: >
            $.resource.properties.region
        - methodMatch: ^setIamPolicy$
          location: PATH
          fieldName: resource
          value: >
            $.resource.self.name
        - methodMatch: ^(update|get|patch|delete)$
          location: PATH
          fieldName: clusterName
          value: >
            $.resource.properties.clusterName
```

- **Step 2**: Create the custom type provider using the following `gcloud` command. Note that you're passing a discovery document[2] to `--descriptor-url` flag. This discovery document is basically doing all the magic of creating a custom type-provider for you. 

> A Discovery Document is a machine-readable specification for describing and consuming REST APIs. It is used to build client libraries, IDE plugins, and other tools that interact with Google APIs. One service may provide multiple discovery documents.  

```
gcloud beta deployment-manager type-providers create dataproc-v1beta --api-options-file dataproc-v1beta.type.yaml --descriptor-url='https://dataproc.googleapis.com/$discovery
/rest?version=v1beta2'

# OUTPUT

Waiting for insert [operation-1584697838999-5a14637c5191b-9deb0532-b1336e26]...done.
Created type_provider [dataproc-v1beta]
```

    - Once this custom GCP type provider `dataproc-v1beta` is created successfully, It will be available for use (just like any other official type provider) in the scope of the GCP project.

- **Step 3**: Now use the custom type provider as `type: {my-project-id}/dataproc-v1beta:projects.regions.clusters` where `{my-project-id}` is the id of your currently active GCP project (where you want to deploy the private dataproc cluster with Presto installation).

- **Step 4**: Then create a jinja template file, say `dataproc.jinja` and paste the following (replace `my-project-name` with the correct project id):

```
resources:
- name: Dataproc-cluster
  type: my-project-name/dataproc-v1beta:projects.regions.clusters
  properties:
    region: { { properties["region"]|safe }}
    projectId: { { env["project"]|safe }}
    clusterName: { { clusterName|safe }}
    config:
      configBucket: example-bucket
      gceClusterConfig:
        zoneUri: https://www.googleapis.com/compute/v1/projects/{ { env["project"]|safe }}/zones/{ { properties["zone"]|safe }}
        tags: 
        - example-firewall-02
        subnetworkUri: https://www.googleapis.com/compute/v1/projects/{ { env["project"]|safe }}/regions//{ { properties["zone"]|safe }}/subnetworks/example-subnet-1
        internalIpOnly: true
      masterConfig:
        numInstances: 1
        machineTypeUri: https://www.googleapis.com/compute/v1/projects/{ { env["project"]|safe }}/zones/{ { properties["zone"]|safe }}/machineTypes/n1-standard-2
        diskConfig:
          bootDiskSizeGb: 200
          bootDiskType: pd-ssd
      workerConfig:
        numInstances: 2
        machineTypeUri: https://www.googleapis.com/compute/v1/projects/{ { env["project"]|safe }}/zones/{ { properties["zone"]|safe }}/machineTypes/n1-standard-2
        diskConfig: 
          bootDiskSizeGb: 200
          bootDiskType: pd-ssd
      softwareConfig:
        imageVersion: 1.4.23-ubuntu18
        optionalComponents: 
        - PRESTO
```
- **Step 5**: Write a `config.yaml` (to test the above jinja template) as following:

```
imports:
- path: dataproc.jinja

resources:
- name: dataproc
  type: dataproc.jinja
  properties:
    region: us-west1
    zone: us-west1-b
```

- **Step 6**: And the final step, create the deployment.

```
cloud deployment-manager deployments create test-dataproc --config=config.yaml
```
---

Ok, it is still highly probable that you might end up getting an error which looks like this

```
message: Required 'deploymentmanager.typeProviders.get' permission for '{{service_account_number}}@cloudservices.gserviceaccount.com
    for resource projects/{{project_name}}/typeProviders/dataproc-v1beta'
```

This is because, your project doesn't have `deploymentmanager.typeProviders.get` role/permission assigned to your deployment manager service account.

So, you need to set-up/assign this role or any [similar superior role](https://cloud.google.com/iam/docs/understanding-roles#deployment-manager-roles) to the deployment manager service account & it should definitely start working for you.

And that's all about it. If everything goes well, you will have a successful dataproc cluster deployment having a PRESTO installation on it, in the end.

*If you still find hard debugging the issues during the process, this issue[1] covers a really detailed troubleshooting discussion around the use-case.*

That's all for now. 

Till next time o/

### REFERENCES:

- [1] Github Issue: [Presto not getting deployed with `type: gcp-types/dataproc-v1:projects.regions.clusters` #546](https://github.com/GoogleCloudPlatform/deploymentmanager-samples/issues/546)
- [2] Discovery Document: [https://dataproc.googleapis.com/$discovery/rest?version=v1beta2](https://dataproc.googleapis.com/$discovery/rest?version=v1beta2)
- [3] [Cloud Dataproc API](https://cloud.google.com/dataproc/docs/reference/rest)
- [4] [Adding an API as a Type Provider](https://cloud.google.com/deployment-manager/docs/configuration/type-providers/creating-type-provider)
- [5] [dataproc-v1](https://cloud.google.com/dataproc/docs/reference/rest/v1/ClusterConfig#Component)
- [6] [dataproc-v1beta2](https://cloud.google.com/dataproc/docs/reference/rest/v1beta2/ClusterConfig#Component)
