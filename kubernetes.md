---
layout: page
title: Kubernetes
heading: ""
---

***First time, I joined the the kubernetes community slack, sometime in the middle of june, 2020.***

***I started there by getting involved with the (then) newly formed, [node-reviewers-group](https://www.psaggu.com/kubernetes-mentorship/2020/07/30/node-reviewer-group-tasks.html). This was kind of a mentorship program where a group of people would work together on reviewing/triaging `sig-node` PR(s) & issue(s).***

***I spent couple of months in the group, trying to understand all what was being taught (or discussed) in there, and then I realised, not much of the stuff made  any sense to me. I was too overwhelmed by the concepts being discussed there, I felt absolutely alien-ish in that space. So, I gave up & left.***

***But fortunately that was not the end for me!***

***I've started again. And this time, I'm very actively getting involved into various parts of the Kubernetes organisation.***


![Screenshot from 2021-05-14 12-05-43](https://user-images.githubusercontent.com/30499743/118231546-f30ca980-b4ac-11eb-9fd8-2d90e6d9e51e.png)


***This will be a running logging document for all my upstream Kubernetes project contributions.***


*(For someone who want to read from the beginning, start [here](https://www.psaggu.com/kubernetes.html#june-2020).)*

---

## *May, 2021*

### **[microsoft/hcsshim](https://github.com/microsoft/hcsshim)**

<sub>`PR(s) merged`
- [bump containerd version to v1.5.1 #1027](https://github.com/microsoft/hcsshim/pull/1027#event-4745184459)</sub>


### **[google/cadvisor](https://github.com/google/cadvisor/)**

- <sub>`PR(s) merged`    
   - [bump containerd version to v1.5.1 #2870](https://github.com/google/cadvisor/pull/2870)</sub>

### **[containerd/zfs](https://github.com/containerd/zfs/)**

- <sub>`PR(s) merged`</sub>
   - [sync up with containerd 1.5 GA #47](https://github.com/containerd/zfs/pull/47)</sub>

### **[kubernetes/image-builder](https://github.com/kubernetes-sigs/image-builder)**

- <sub>`PR(s) merged`</sub>
   - [bump containerd version to v1.5.1 #610](https://github.com/kubernetes-sigs/image-builder/pull/610)</sub>
   - [bump containerd version to v1.5.0 #606](https://github.com/kubernetes-sigs/image-builder/pull/606)</sub>


### **[kubernetes/test-infra](https://github.com/kubernetes/test-infra)**

- <sub>`PR(s) merged`</sub>
   - [bump containerd version to v1.5.1 #22178](https://github.com/kubernetes/test-infra/pull/22178)</sub>
   - [bump containerd version to v1.5.0 #22157](https://github.com/kubernetes/test-infra/pull/22157)</sub>

### **[ kubernetes-client/python ](https://github.com/kubernetes-client/python)**</sub>

- `PR(s) merged`:</sub>
    - [add examples to demonstrate the usage of dynamic client #1448](https://github.com/kubernetes-client/python/pull/1448)</sub>
    - [add example to demonstrate a rolling restart of the deployment #1450](https://github.com/kubernetes-client/python/pull/1450)</sub>
    - [update deployment_crud.py to include a restart_deployment method for typed client #1452](https://github.com/kubernetes-client/python/pull/1452)</sub>
    - [add 'list_ingressroute_for_all_namespaces' method #1454](https://github.com/kubernetes-client/python/pull/1454)</sub>

- <sub>`Issues resolved`:</sub>
    - <sub>[Dynamic client example #1429](https://github.com/kubernetes-client/python/issues/1429)</sub>
    - <sub>[How do we do rolling restart?#1378](https://github.com/kubernetes-client/python/issues/1378)</sub>
    - <sub>[how to get namespaces ingressroutes through #1388](https://github.com/kubernetes-client/python/issues/1388)</sub>

- `Issues assigned`:</sub>
    -  <sub>[Document client-side timeouts in watch #1402](https://github.com/kubernetes-client/python/issues/1402)</sub>
    -  <sub>[Drop Python 2 support #1413](https://github.com/kubernetes-client/python/issues/1413)</sub>

---

## *April, 2021*

### **[ kubernetes-client/python ](https://github.com/kubernetes-client/python)**

- <sub>`PRs raised`:</sub>
    - <sub>[Add example to demonstrate usage of patch_cluster_custom_object method #1437](https://github.com/kubernetes-client/python/pull/1437)</sub>
    - <sub>[simplify & enhance the node_labels.py example #1435](https://github.com/kubernetes-client/python/pull/1435)</sub>
    - <sub>[Fix CustomResourceDefinition manifest yaml in custom_object.py example #1433 ](https://github.com/kubernetes-client/python/pull/1433)</sub>
    
- `Issues resolved`:</sub>
    - [Example of body format for patch_cluster_custom_object #1427](https://github.com/kubernetes-client/python/issues/1427)</sub>

   
- <sub>`Issues created & resolved`:
    - <sub>[Improve the custom_object.py to be more specific to usage of namespaced custom resource #1438](https://github.com/kubernetes-client/python/issues/1438)</sub>
    - <sub>[Update the CRD yaml manifest mentioned in custom_object example #1432](https://github.com/kubernetes-client/python/issues/1432)</sub>
    - <sub>[simplify & enhance the node_labels.py example #1434](https://github.com/kubernetes-client/python/issues/1434)</sub>

- <sub>`Issues/PRs responded to`:</sub>
    -  <sub>[Removed custom_object.py and created a new file namespaced</sub>_custom_object.py which is more specific to usage of namespaced custom resource #1440](https://github.com/kubernetes-client/python/pull/1440)

---

## *March, 2021*

### **[integreatly-operator](https://github.com/integr8ly/integreatly-operator)**</sub>

<sub>I first started writing kubernetes flavor of go code while working on the [integreatly-operator](https://github.com/integr8ly/integreatly-operator) project. This is an Openshift Operator based on the Operator SDK for installing and reconciling Integreatly services.</sub>


- <sub>`PR(s) merged`</sub>

    - <sub>[Add custom alertmanager go template to enhance email config #1721](https://github.com/integr8ly/integreatly-operator/pull/1721)</sub>
    - <sub>[Add alertmanager config changes #1672](https://github.com/integr8ly/integreatly-operator/pull/1672)</sub>
    - <sub>[fix hardcoded addon value in controllers/rhmi/promethuesRules.go #1649](https://github.com/integr8ly/integreatly-operator/pull/1649)</sub>

---

## *June, 2020*

#### **[kubernetes/community](https://github.com/kubernetes/community/)**

<sub>This was my very first time contributing on the upstream kubernetes project.</sub>

- <sub>`PR(s) merged`</sub>

    - <sub>[Update broken file link in title 3 #4896](https://github.com/kubernetes/community/pull/4896)</sub>
