---
layout: page
title: K8s Contributions
heading: ""
---

<sub>***First time, I joined the the kubernetes community slack, sometime in the middle of june, 2020.***</sub>

<sub>***I started there by getting involved with the (then) newly formed, [node-reviewers-group](https://www.psaggu.com/kubernetes-mentorship/2020/07/30/node-reviewer-group-tasks.html). This was kind of a mentorship program where a group of people would work together on reviewing/triaging `sig-node` PR(s) & issue(s).***</sub>

<sub>***I spent couple of months in the group, trying to understand all what was being taught (or discussed) in there. I soon realised I was not able to understand much of the stuff at the time. I was too overwhelmed by the concepts being discussed there, that I felt absolutely alien-ish in that space. So, in the end, I just gave up & left.***</sub>

<sub>***Which was not good, I should have tried more. But anyway, I'm back on the track after 6 months now!***</sub>

***I've started my journey again. And this time, I'm very actively getting involved into various parts of the Kubernetes organisation.***


![psaggu-k8s-logo](https://user-images.githubusercontent.com/30499743/118231546-f30ca980-b4ac-11eb-9fd8-2d90e6d9e51e.png)


***This document will be a running logging document for all my upstream Kubernetes project contributions.***

***So, Let's start then...***


*(For someone who want to read from the beginning, start [here](https://www.psaggu.com/kubernetes.html#june-2020).)*

---

# *June, 2021*

#### **[stackrox/kube-linter](https://github.com/stackrox/kube-linter)**

- `PR(s) raised`
    - <sub>[add check for validating improper container image tags #191](https://github.com/stackrox/kube-linter/pull/191/files)</sub>


---

# *May, 2021*

#### **[kubernetes/website](https://github.com/kubernetes/website)**

- `PR(s) merged`
    - <sub>[fix the kubelet-config-1.21 configmap key value from config to kubelet #28025](https://github.com/kubernetes/website/pull/28025)</sub>

---

- `Issues resolved`
    - <sub>[Issue with k8s.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/ #27931](https://github.com/kubernetes/website/issues/27931)</sub>

---

- `Issues reviewed/triaged`  
    - <sub>[Delete a StatefulSet #27920](https://github.com/kubernetes/website/issues/27920)</sub>
    - <sub>[Install and Set Up kubectl on Linux #27951](https://github.com/kubernetes/website/issues/27951#issuecomment-844218003)</sub>     
    - <sub>[Last command of "Interactive Tutorial - Exposing Your App" interactive lesson is deprecated #27056](https://github.com/kubernetes/website/issues/27056#issuecomment-843129207)</sub>
    - <sub>[List All Container Images Running in a Cluster (#27475)](https://github.com/kubernetes/website/issues/27475#issuecomment-843066458)</sub>
    - <sub>[Non-existent script is being referenced #27982](https://github.com/kubernetes/website/issues/27982#issuecomment-844272373)</sub>
    - <sub>[Unclear requirements for “Using Source IP” tutorial #27162](https://github.com/kubernetes/website/issues/27162#issuecomment-843223669)</sub>

---

#### **[kubernetes/org](https://github.com/kubernetes/org)**

- `kubernetes organisation membership request` 🎊
    - <sub>[REQUEST: New membership for Priyankasaggu11929 #2712](https://github.com/kubernetes/org/issues/2712)</sub>
    - <sub>[add Priyankasaggu11929 to wg-structured-logging #2739](https://github.com/kubernetes/org/pull/2739)</sub>

---

#### **[kubernetes-client/python-base](https://github.com/kubernetes-client/python-base)**

- `PR(s) merged`
    - <sub>[drop python2 support #238](https://github.com/kubernetes-client/python-base/pull/238)</sub>

---

#### **[containerd/containerd](https://github.com/containerd/containerd)**

- `PR(s) merged`
    - <sub>[bump runc version to v1.0.0-rc95 #5514](https://github.com/containerd/containerd/pull/5514)</sub>
    - <sub>[bump hcsshim version to v0.8.17 #5505](https://github.com/containerd/containerd/pull/5505)</sub>
 
---

#### **[microsoft/hcsshim](https://github.com/microsoft/hcsshim)**

- `PR(s) merged`
    - <sub>[bump containerd version to v1.5.1 #1027](https://github.com/microsoft/hcsshim/pull/1027#event-4745184459)</sub>
 
---


#### **[google/cadvisor](https://github.com/google/cadvisor/)**

- `PR(s) merged`
    - <sub>[bump runc version to v1.0.0-rc95 #2873](https://github.com/google/cadvisor/pull/2873)</sub>
    - <sub>[bump containerd version to v1.5.1 #2870](https://github.com/google/cadvisor/pull/2870)</sub>

---

#### **[containerd/zfs](https://github.com/containerd/zfs/)**

- `PR(s) merged`
    - <sub>[sync up with containerd 1.5 GA #47](https://github.com/containerd/zfs/pull/47)</sub>

---

#### **[kubernetes/image-builder](https://github.com/kubernetes-sigs/image-builder)**

- `PR(s) merged`
    - <sub>[bump containerd version to v1.5.1 #610](https://github.com/kubernetes-sigs/image-builder/pull/610)</sub>
    - <sub>[bump containerd version to v1.5.0 #606](https://github.com/kubernetes-sigs/image-builder/pull/606)</sub>

---


#### **[kubernetes/test-infra](https://github.com/kubernetes/test-infra)**

- `PR(s) merged`  
    - <sub>[bump runc version to v1.0.0-rc95 & containerd version to v1.5.2 #22273](https://github.com/kubernetes/test-infra/pull/22273)</sub>
    - <sub>[bump containerd version to v1.5.1 #22178](https://github.com/kubernetes/test-infra/pull/22178)</sub>
    - <sub>[bump containerd version to v1.5.0 #22157](https://github.com/kubernetes/test-infra/pull/22157)</sub>

---

#### **[kubernetes-client/python](https://github.com/kubernetes-client/python)**

- `WIP PR(s)`
    - <sub>[[WIP] add documentation for the server & client side timeout #1467](https://github.com/kubernetes-client/python/pull/1467)</sub>

- `PR(s) merged`
    - <sub>[drop python 2 support #1468](https://github.com/kubernetes-client/python/pull/1468)</sub> 
    - <sub>[add examples to demonstrate the usage of dynamic client #1448](https://github.com/kubernetes-client/python/pull/1448)</sub>
    - <sub>[add example to demonstrate a rolling restart of the deployment #1450](https://github.com/kubernetes-client/python/pull/1450)</sub>
    - <sub>[update deployment_crud.py to include a restart_deployment method for typed client #1452](https://github.com/kubernetes-client/python/pull/1452)</sub>
    - <sub>[add 'list_ingressroute_for_all_namespaces' method #1454](https://github.com/kubernetes-client/python/pull/1454)</sub>

- `Issues resolved`
    - <sub>[Dynamic client example #1429](https://github.com/kubernetes-client/python/issues/1429)</sub>
    - <sub>[How do we do rolling restart?#1378](https://github.com/kubernetes-client/python/issues/1378)</sub>
    - <sub>[how to get namespaces ingressroutes through #1388](https://github.com/kubernetes-client/python/issues/1388)</sub>

- `Issues assigned`
    - <sub>[Document client-side timeouts in watch #1402](https://github.com/kubernetes-client/python/issues/1402)</sub>
    - <sub>[Drop Python 2 support #1413](https://github.com/kubernetes-client/python/issues/1413)</sub>

---

# *April, 2021*

#### **[kubernetes-client/python](https://github.com/kubernetes-client/python)**

- `PRs raised`
    - <sub>[Add example to demonstrate usage of patch_cluster_custom_object method #1437](https://github.com/kubernetes-client/python/pull/1437)</sub>
    - <sub>[simplify & enhance the node_labels.py example #1435](https://github.com/kubernetes-client/python/pull/1435)</sub>
    - <sub>[Fix CustomResourceDefinition manifest yaml in custom_object.py example #1433 ](https://github.com/kubernetes-client/python/pull/1433)</sub>

- `Issues resolved`
    - <sub>[Example of body format for patch_cluster_custom_object #1427](https://github.com/kubernetes-client/python/issues/1427)</sub>

   
- `Issues created & resolved`
    - <sub>[Improve the custom_object.py to be more specific to usage of namespaced custom resource #1438](https://github.com/kubernetes-client/python/issues/1438)</sub>
    - <sub>[Update the CRD yaml manifest mentioned in custom_object example #1432](https://github.com/kubernetes-client/python/issues/1432)</sub>
    - <sub>[simplify & enhance the node_labels.py example #1434](https://github.com/kubernetes-client/python/issues/1434)</sub>

- `Issues/PRs responded to`
    - <sub>[Removed custom_object.py and created a new file namespaced</sub>_custom_object.py which is more specific to usage of namespaced custom resource #1440](https://github.com/kubernetes-client/python/pull/1440)

---

# *March, 2021*

#### **[integreatly-operator](https://github.com/integr8ly/integreatly-operator)**

<sub>I first started writing kubernetes flavor of go code while working on the [integreatly-operator](https://github.com/integr8ly/integreatly-operator) project. This is an Openshift Operator based on the Operator SDK for installing and reconciling Integreatly services.</sub>

- `PR(s) merged`

    - <sub>[Add custom alertmanager go template to enhance email config #1721](https://github.com/integr8ly/integreatly-operator/pull/1721)</sub>
    - <sub>[Add alertmanager config changes #1672](https://github.com/integr8ly/integreatly-operator/pull/1672)</sub>
    - <sub>[fix hardcoded addon value in controllers/rhmi/promethuesRules.go #1649](https://github.com/integr8ly/integreatly-operator/pull/1649)</sub>

---

# *June, 2020*

#### **[kubernetes/community](https://github.com/kubernetes/community/)**

<sub>This was my very first time contributing on the upstream kubernetes project.</sub>

- `PR(s) merged`

    - <sub>[Update broken file link in title 3 #4896](https://github.com/kubernetes/community/pull/4896)</sub>
