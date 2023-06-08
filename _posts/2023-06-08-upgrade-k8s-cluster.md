---
layout: post
title: "Upgrading Kubernetes Cluster"
description: ""
category: 
tags: []
comments: false

---

June 08, 2023

---

**Disclaimer:**  

_Just trying to document the process (strictly) for me._

_This documentation is just for educational purpose._

_**The process won't follow for any production cluster!**_

## Aim

To upgrade a Kubernetes cluster with nodes running Kubernetes Version v1.26.4 to v1.27.2

I'm using a Kubernetes cluster created using Kind, for the example sake.

### [STEP 1] Create a kind Kubernetes cluster

Use the following `kind-config.yaml` file:

```yaml
# three node (two workers) cluster config
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  image: kindest/node:v1.26.4@sha256:f4c0d87be03d6bea69f5e5dc0adb678bb498a190ee5c38422bf751541cebe92e
- role: worker
  image: kindest/node:v1.26.4@sha256:f4c0d87be03d6bea69f5e5dc0adb678bb498a190ee5c38422bf751541cebe92e
```

Please note:
- The above config file for Kind cluster will create a Kubernetes cluster with 2 nodes:
    - Control Plane Node (name: kind-control-plane)
      Kubernetes Version: v1.26.4
    - Worker Node (name: kind-worker)
      Kubernetes Version: v1.26.4
      
**Run the following command to create the cluster:**

```bash
$ kind create cluster --config kind-config.yaml 
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.26.4) 🖼
 ✓ Preparing nodes 📦 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
 ✓ Joining worker nodes 🚜 
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Have a question, bug, or feature request? Let us know! https://kind.sigs.k8s.io/#community 🙂
```

**Verify if cluster came up successfully:**

```bash
$ kubectl get nodes -o wide

NAME                 STATUS   ROLES           AGE     VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION      CONTAINER-RUNTIME
kind-control-plane   Ready    control-plane   2m43s   v1.26.4   172.18.0.3    <none>        Debian GNU/Linux 11 (bullseye)   5.15.0-73-generic   containerd://1.6.21
kind-worker          Ready    <none>          2m25s   v1.26.4   172.18.0.2    <none>        Debian GNU/Linux 11 (bullseye)   5.15.0-73-generic   containerd://1.6.21

```

Note that the version of both nodes is currently `v1.26.4`

---

### [STEP 2] Upgrade the control plane node

**Exec inside the docker container corresponding to the control plane node (kind-control-plane):**

```bash
$ docker exec -it kind-control-plane bash

root@kind-control-plane:/# 
```

**Install the utility packages:**

```bash
root@kind-control-plane:/# apt-get update && apt-get install -y apt-transport-https curl gnupg
root@kind-control-plane:/# curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
root@kind-control-plane:/# cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
root@kind-control-plane:/# apt-get update
```

**Check which version to upgrade to (in our case, we're checking if v1.27.2 is available)**

```bash
root@kind-control-plane:/# apt-cache madison kubeadm

  kubeadm |  1.27.2-00 | http://apt.kubernetes.io kubernetes-xenial/main amd64 Packages
  kubeadm |  1.27.1-00 | http://apt.kubernetes.io kubernetes-xenial/main amd64 Packages
  kubeadm |  1.27.0-00 | http://apt.kubernetes.io kubernetes-xenial/main amd64 Packages
  kubeadm |  1.26.5-00 | http://apt.kubernetes.io kubernetes-xenial/main amd64 Packages
  kubeadm |  1.26.4-00 | http://apt.kubernetes.io kubernetes-xenial/main amd64 Packages
  ...
```

**Upgrade Kubeadm to the required version:**

```bash
root@kind-control-plane:/# apt-mark unhold kubeadm && apt-get update && apt-get install -y kubeadm=1.27.2-00 && apt-mark hold kubeadm

...
Setting up kubeadm (1.27.2-00) ...

Configuration file '/etc/systemd/system/kubelet.service.d/10-kubeadm.conf'
 ==> File on system created by you or by a script.
 ==> File also in package provided by package maintainer.
   What would you like to do about it ?  Your options are:
    Y or I  : install the package maintainer's version
    N or O  : keep your currently-installed version
      D     : show the differences between the versions
      Z     : start a shell to examine the situation
 The default action is to keep your current version.
*** 10-kubeadm.conf (Y/I/N/O/D/Z) [default=N] ? Y
Installing new version of config file /etc/systemd/system/kubelet.service.d/10-kubeadm.conf ...
kubeadm set on hold.
...

root@kind-control-plane:/# kubeadm version

kubeadm version: &version.Info{Major:"1", Minor:"27", GitVersion:"v1.27.2", GitCommit:"7f6f68fdabc4df88cfea2dcf9a19b2b830f1e647", GitTreeState:"clean", BuildDate:"2023-05-17T14:18:49Z", GoVersion:"go1.20.4", Compiler:"gc", Platform:"linux/amd64"}
```

**Check & Verify the Kubeadm upgrade plan:**

```bash
root@kind-control-plane:/# kubeadm upgrade plan
[upgrade/config] Making sure the configuration is correct:
[upgrade/config] Reading configuration from the cluster...
[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[preflight] Running pre-flight checks.
[upgrade] Running cluster health checks
[upgrade] Fetching available versions to upgrade to
[upgrade/versions] Cluster version: v1.26.4
[upgrade/versions] kubeadm version: v1.27.2
[upgrade/versions] Target version: v1.27.2
[upgrade/versions] Latest version in the v1.26 series: v1.26.5
W0608 12:57:04.800282    5535 compute.go:307] [upgrade/versions] could not find officially supported version of etcd for Kubernetes v1.27.2, falling back to the nearest etcd version (3.5.7-0)

Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
COMPONENT   CURRENT       TARGET
kubelet     1 x v1.26.4   v1.26.5
            1 x v1.27.2   v1.26.5

Upgrade to the latest version in the v1.26 series:

COMPONENT                 CURRENT   TARGET
kube-apiserver            v1.26.4   v1.26.5
kube-controller-manager   v1.26.4   v1.26.5
kube-scheduler            v1.26.4   v1.26.5
kube-proxy                v1.26.4   v1.26.5
CoreDNS                   v1.9.3    v1.10.1
etcd                      3.5.6-0   3.5.7-0

You can now apply the upgrade by executing the following command:

	kubeadm upgrade apply v1.26.5

_____________________________________________________________________

Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
COMPONENT   CURRENT       TARGET
kubelet     1 x v1.26.4   v1.27.2
            1 x v1.27.2   v1.27.2

Upgrade to the latest stable version:

COMPONENT                 CURRENT   TARGET
kube-apiserver            v1.26.4   v1.27.2
kube-controller-manager   v1.26.4   v1.27.2
kube-scheduler            v1.26.4   v1.27.2
kube-proxy                v1.26.4   v1.27.2
CoreDNS                   v1.9.3    v1.10.1
etcd                      3.5.6-0   3.5.7-0

You can now apply the upgrade by executing the following command:

	kubeadm upgrade apply v1.27.2

_____________________________________________________________________


The table below shows the current state of component configs as understood by this version of kubeadm.
Configs that have a "yes" mark in the "MANUAL UPGRADE REQUIRED" column require manual config upgrade or
resetting to kubeadm defaults before a successful upgrade can be performed. The version to manually
upgrade to is denoted in the "PREFERRED VERSION" column.

API GROUP                 CURRENT VERSION   PREFERRED VERSION   MANUAL UPGRADE REQUIRED
kubeproxy.config.k8s.io   v1alpha1          v1alpha1            no
kubelet.config.k8s.io     v1beta1           v1beta1             no
_____________________________________________________________________

```

**We will upgrade to the late stable version (v1.27.2):**

```bash
root@kind-control-plane:/# kubeadm upgrade apply v1.27.2

[upgrade/config] Making sure the configuration is correct:
[upgrade/config] Reading configuration from the cluster...
[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[preflight] Running pre-flight checks.
[upgrade] Running cluster health checks
[upgrade/version] You have chosen to change the cluster version to "v1.27.2"
[upgrade/versions] Cluster version: v1.26.4
[upgrade/versions] kubeadm version: v1.27.2
[upgrade] Are you sure you want to proceed? [y/N]: y
[upgrade/prepull] Pulling images required for setting up a Kubernetes cluster
[upgrade/prepull] This might take a minute or two, depending on the speed of your internet connection
[upgrade/prepull] You can also perform this action in beforehand using 'kubeadm config images pull'
W0608 12:59:23.499649    5571 images.go:80] could not find officially supported version of etcd for Kubernetes v1.27.2, falling back to the nearest etcd version (3.5.7-0)
W0608 13:00:07.900906    5571 checks.go:835] detected that the sandbox image "registry.k8s.io/pause:3.7" of the container runtime is inconsistent with that used by kubeadm. It is recommended that using "registry.k8s.io/pause:3.9" as the CRI sandbox image.
[upgrade/apply] Upgrading your Static Pod-hosted control plane to version "v1.27.2" (timeout: 5m0s)...
[upgrade/etcd] Upgrading to TLS for etcd
W0608 13:00:48.303106    5571 staticpods.go:305] [upgrade/etcd] could not find officially supported version of etcd for Kubernetes v1.27.2, falling back to the nearest etcd version (3.5.7-0)
W0608 13:00:48.305410    5571 images.go:80] could not find officially supported version of etcd for Kubernetes v1.27.2, falling back to the nearest etcd version (3.5.7-0)
[upgrade/staticpods] Preparing for "etcd" upgrade
[upgrade/staticpods] Renewing etcd-server certificate
[upgrade/staticpods] Renewing etcd-peer certificate
[upgrade/staticpods] Renewing etcd-healthcheck-client certificate
[upgrade/staticpods] Moved new manifest to "/etc/kubernetes/manifests/etcd.yaml" and backed up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2023-06-08-13-00-48/etcd.yaml"
[upgrade/staticpods] Waiting for the kubelet to restart the component
[upgrade/staticpods] This might take a minute or longer depending on the component/version gap (timeout 5m0s)
[apiclient] Found 1 Pods for label selector component=etcd
[upgrade/staticpods] Component "etcd" upgraded successfully!
[upgrade/etcd] Waiting for etcd to become available
[upgrade/staticpods] Writing new Static Pod manifests to "/etc/kubernetes/tmp/kubeadm-upgraded-manifests56128700"
[upgrade/staticpods] Preparing for "kube-apiserver" upgrade
[upgrade/staticpods] Renewing apiserver certificate
[upgrade/staticpods] Renewing apiserver-kubelet-client certificate
[upgrade/staticpods] Renewing front-proxy-client certificate
[upgrade/staticpods] Renewing apiserver-etcd-client certificate
[upgrade/staticpods] Moved new manifest to "/etc/kubernetes/manifests/kube-apiserver.yaml" and backed up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2023-06-08-13-00-48/kube-apiserver.yaml"
[upgrade/staticpods] Waiting for the kubelet to restart the component
[upgrade/staticpods] This might take a minute or longer depending on the component/version gap (timeout 5m0s)
[apiclient] Found 1 Pods for label selector component=kube-apiserver
[upgrade/staticpods] Component "kube-apiserver" upgraded successfully!
[upgrade/staticpods] Preparing for "kube-controller-manager" upgrade
[upgrade/staticpods] Renewing controller-manager.conf certificate
[upgrade/staticpods] Moved new manifest to "/etc/kubernetes/manifests/kube-controller-manager.yaml" and backed up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2023-06-08-13-00-48/kube-controller-manager.yaml"
[upgrade/staticpods] Waiting for the kubelet to restart the component
[upgrade/staticpods] This might take a minute or longer depending on the component/version gap (timeout 5m0s)
[apiclient] Found 1 Pods for label selector component=kube-controller-manager
[upgrade/staticpods] Component "kube-controller-manager" upgraded successfully!
[upgrade/staticpods] Preparing for "kube-scheduler" upgrade
[upgrade/staticpods] Renewing scheduler.conf certificate
[upgrade/staticpods] Moved new manifest to "/etc/kubernetes/manifests/kube-scheduler.yaml" and backed up old manifest to "/etc/kubernetes/tmp/kubeadm-backup-manifests-2023-06-08-13-00-48/kube-scheduler.yaml"
[upgrade/staticpods] Waiting for the kubelet to restart the component
[upgrade/staticpods] This might take a minute or longer depending on the component/version gap (timeout 5m0s)
[apiclient] Found 1 Pods for label selector component=kube-scheduler
[upgrade/staticpods] Component "kube-scheduler" upgraded successfully!
[upload-config] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config" in namespace kube-system with the configuration for the kubelets in the cluster
[upgrade] Backing up kubelet config file to /etc/kubernetes/tmp/kubeadm-kubelet-config2613181160/config.yaml
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to get nodes
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

[upgrade/successful] SUCCESS! Your cluster was upgraded to "v1.27.2". Enjoy!

[upgrade/kubelet] Now that your control plane is upgraded, please proceed with upgrading your kubelets if you haven't already done so.
```

**I'm skipping upgrading the CNI** (I don't have any additional CNI provider plugin, other than what defaults to Kind cluster ~ [kindnet](https://github.com/kubernetes-sigs/kind/tree/main/images/kindnetd))

But if you need to check how kindnet is working, do following inside the control plane node:

```bash
root@kind-control-plane:/# crictl ps

...
5715f2f6e401c       b0b1fa0f58c6e       8 minutes ago       Running             kindnet-cni               2                   3d78434184edf       kindnet-blltq
...
root@kind-control-plane:/# crictl logs 5715f2f6e401c   
I0608 13:02:38.079089       1 main.go:316] probe TCP address kind-control-plane:6443
W0608 13:02:38.080550       1 main.go:332] REFUSED kind-control-plane:6443
I0608 13:02:38.080592       1 main.go:93] apiserver not reachable, attempt 0 ... retrying
I0608 13:02:38.080600       1 main.go:316] probe TCP address kind-control-plane:6443
W0608 13:02:38.081047       1 main.go:332] REFUSED kind-control-plane:6443
I0608 13:02:38.081072       1 main.go:93] apiserver not reachable, attempt 1 ... retrying
I0608 13:02:39.081260       1 main.go:316] probe TCP address kind-control-plane:6443
W0608 13:02:39.082375       1 main.go:332] REFUSED kind-control-plane:6443
I0608 13:02:39.082405       1 main.go:93] apiserver not reachable, attempt 2 ... retrying
I0608 13:02:41.082727       1 main.go:316] probe TCP address kind-control-plane:6443
W0608 13:02:41.083924       1 main.go:332] REFUSED kind-control-plane:6443
I0608 13:02:41.083963       1 main.go:93] apiserver not reachable, attempt 3 ... retrying
I0608 13:02:44.085510       1 main.go:316] probe TCP address kind-control-plane:6443
I0608 13:02:44.088241       1 main.go:102] connected to apiserver: https://kind-control-plane:6443
I0608 13:02:44.088270       1 main.go:107] hostIP = 172.18.0.3
podIP = 172.18.0.3
I0608 13:02:44.088459       1 main.go:116] setting mtu 1500 for CNI 
I0608 13:02:44.088536       1 main.go:146] kindnetd IP family: "ipv4"
I0608 13:02:44.088559       1 main.go:150] noMask IPv4 subnets: [10.244.0.0/16]
I0608 13:02:44.278193       1 main.go:223] Handling node with IPs: map[172.18.0.3:{}]
I0608 13:02:44.278210       1 main.go:227] handling current node
I0608 13:02:44.280741       1 main.go:223] Handling node with IPs: map[172.18.0.2:{}]
I0608 13:02:44.280753       1 main.go:250] Node kind-worker has CIDR [10.244.1.0/24] 
I0608 13:02:54.293198       1 main.go:223] Handling node with IPs: map[172.18.0.3:{}]
```

Now, before we go and upgrade the kubelet & kubectl (& restart the services), 

**Open a new terminal (outside the docker exec) and mark the node unschedulable (cordon) and then evict the workload (drain)**

```bash
# Outside the docker exec terminal
$ kubectl drain kind-control-plane --ignore-daemonsets

node/kind-control-plane cordoned
Warning: ignoring DaemonSet-managed Pods: kube-system/kindnet-blltq, kube-system/kube-proxy-rfbd5
evicting pod local-path-storage/local-path-provisioner-6bd6454576-xlvmc
pod/local-path-provisioner-6bd6454576-xlvmc evicted
node/kind-control-plane drained

$ kubectl get nodes -o wide

NAME                 STATUS                     ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION      CONTAINER-RUNTIME
kind-control-plane   Ready,SchedulingDisabled   control-plane   47m   v1.27.2   172.18.0.3    <none>        Debian GNU/Linux 11 (bullseye)   5.15.0-73-generic   containerd://1.6.21
kind-worker          Ready                      <none>          47m   v1.26.4   172.18.0.2    <none>        Debian GNU/Linux 11 (bullseye)   5.15.0-73-generic   containerd://1.6.21

```

**Now, come back to the former terminal with the docker exec (into control-plane node):**

**And upgrade the kubelet and kubectl:**

```bash
root@kind-control-plane:/# apt-mark unhold kubelet kubectl && apt-get update && apt-get install -y kubelet=1.27.2-00 kubectl=1.27.2-00 && apt-mark hold kubelet kubectl

kubelet was already not hold.
kubectl was already not hold.
Hit:2 http://deb.debian.org/debian bullseye InRelease
Hit:3 http://deb.debian.org/debian-security bullseye-security InRelease             
Hit:4 http://deb.debian.org/debian bullseye-updates InRelease                       
Hit:1 https://packages.cloud.google.com/apt kubernetes-xenial InRelease             
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
kubectl is already the newest version (1.27.2-00).
kubectl set to manually installed.
kubelet is already the newest version (1.27.2-00).
kubelet set to manually installed.
0 upgraded, 0 newly installed, 0 to remove and 2 not upgraded.
kubelet set on hold.
```

**And now restart the kubelet:**

```bash
root@kind-control-plane:/# systemctl daemon-reload
root@kind-control-plane:/# systemctl restart kubelet
```

**And now go back to the other terminal outside the docker exec, and uncordon the node:**

```bash
$ kubectl uncordon kind-control-plane

node/kind-control-plane uncordoned
```

And that's everything for the control plane upgrade! Just check at last if it is running properly!

```bash
$ kubectl get nodes -o wide

NAME                 STATUS   ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION      CONTAINER-RUNTIME
kind-control-plane   Ready    control-plane   52m   v1.27.2   172.18.0.3    <none>        Debian GNU/Linux 11 (bullseye)   5.15.0-73-generic   containerd://1.6.21
kind-worker          Ready    <none>          51m   v1.26.4   172.18.0.2    <none>        Debian GNU/Linux 11 (bullseye)   5.15.0-73-generic   containerd://1.6.21
```

**And don't forget to exit from the docker exec terminal (kind-control-plane):**

```bash
root@kind-control-plane:/# exit
exit
```

---

### [STEP 3] Upgrade the worker node

**Exec inside the docker container corresponding to the worker node (kind-worker):**

```bash
$ docker exec -it kind-worker bash
root@kind-worker:/# 
```

**Install the utility packages:**

```bash
root@kind-worker:/#  apt-get update && apt-get install -y apt-transport-https curl gnupg
root@kind-worker:/#  curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
root@kind-worker:/#  cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
root@kind-worker:/#  apt-get update
```

**Upgrade Kubeadm to the required version:**

```bash
root@kind-worker:/# apt-mark unhold kubeadm && apt-get update && apt-get install -y kubeadm=1.27.2-00 && apt-mark hold kubeadm

...
Setting up kubeadm (1.27.2-00) ...

Configuration file '/etc/systemd/system/kubelet.service.d/10-kubeadm.conf'
 ==> File on system created by you or by a script.
 ==> File also in package provided by package maintainer.
   What would you like to do about it ?  Your options are:
    Y or I  : install the package maintainer's version
    N or O  : keep your currently-installed version
      D     : show the differences between the versions
      Z     : start a shell to examine the situation
 The default action is to keep your current version.
*** 10-kubeadm.conf (Y/I/N/O/D/Z) [default=N] ? Y
Installing new version of config file /etc/systemd/system/kubelet.service.d/10-kubeadm.conf ...
kubeadm set on hold.
```

**Run kubeadm upgrade (For worker nodes this upgrades the local kubelet configuration):**

```bash
root@kind-worker:/# kubeadm upgrade node

[upgrade] Reading configuration from the cluster...
[upgrade] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[preflight] Running pre-flight checks
[preflight] Skipping prepull. Not a control plane node.
[upgrade] Skipping phase. Not a control plane node.
[upgrade] Backing up kubelet config file to /etc/kubernetes/tmp/kubeadm-kubelet-config2909228160/config.yaml
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[upgrade] The configuration for this node was successfully updated!
[upgrade] Now you should go ahead and upgrade the kubelet package using your package manager.
```

Now, before we go and upgrade the kubelet & kubectl (& restart the services), 

**Open a new terminal (outside the docker exec of kind-worker container) and mark the node unschedulable (cordon) and then evict the workload (drain)**

```bash
# Outside the docker exec terminal
$ kubectl drain kind-worker --ignore-daemonsets

node/kind-worker cordoned
Warning: ignoring DaemonSet-managed Pods: kube-system/kindnet-qpx8l, kube-system/kube-proxy-5xf5d
evicting pod local-path-storage/local-path-provisioner-6bd6454576-km824
evicting pod kube-system/coredns-5d78c9869d-mvgjq
evicting pod kube-system/coredns-5d78c9869d-zrmm4
pod/coredns-5d78c9869d-mvgjq evicted
pod/coredns-5d78c9869d-zrmm4 evicted
pod/local-path-provisioner-6bd6454576-km824 evicted
node/kind-worker drained

$ kubectl get nodes -o wide
NAME                 STATUS                     ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION      CONTAINER-RUNTIME
kind-control-plane   Ready                      control-plane   62m   v1.27.2   172.18.0.3    <none>        Debian GNU/Linux 11 (bullseye)   5.15.0-73-generic   containerd://1.6.21
kind-worker          Ready,SchedulingDisabled   <none>          61m   v1.27.2   172.18.0.2    <none>        Debian GNU/Linux 11 (bullseye)   5.15.0-73-generic   containerd://1.6.21
```

**Now, come back to the former terminal with the docker exec (into kind-worker container):**

**And upgrade the kubelet and kubectl:**

```bash
root@kind-control-plane:/# apt-mark unhold kubelet kubectl && apt-get update && apt-get install -y kubelet=1.27.2-00 kubectl=1.27.2-00 && apt-mark hold kubelet kubectl

kubelet was already not hold.
kubectl was already not hold.
Hit:2 http://deb.debian.org/debian bullseye InRelease            
Hit:3 http://deb.debian.org/debian-security bullseye-security InRelease
Hit:4 http://deb.debian.org/debian bullseye-updates InRelease                      
Hit:1 https://packages.cloud.google.com/apt kubernetes-xenial InRelease            
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
kubectl is already the newest version (1.27.2-00).
kubectl set to manually installed.
kubelet is already the newest version (1.27.2-00).
kubelet set to manually installed.
0 upgraded, 0 newly installed, 0 to remove and 2 not upgraded.
kubelet set on hold.
kubectl set on hold.
```

**And now restart the kubelet:**

```bash
root@kind-worker:/# systemctl daemon-reload
root@kind-worker:/# systemctl restart kubelet
```

**And now go back to the other terminal outside the docker exec, and uncordon the node:**

```bash
$ kubectl uncordon kind-worker

node/kind-worker uncordoned
```

And that's everything for the worker node upgrade! Just check at last if it is running properly!

```bash
$ kubectl get nodes -o wide
NAME                 STATUS   ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION      CONTAINER-RUNTIME
kind-control-plane   Ready    control-plane   67m   v1.27.2   172.18.0.3    <none>        Debian GNU/Linux 11 (bullseye)   5.15.0-73-generic   containerd://1.6.21
kind-worker          Ready    <none>          66m   v1.27.2   172.18.0.2    <none>        Debian GNU/Linux 11 (bullseye)   5.15.0-73-generic   containerd://1.6.21
```

**And don't forget to exit from the docker exec terminal (kind-worker):**

```bash
root@kind-worker:/# exit
exit
```

With that both our nodes are now successfully upgraded from Kubernetes version v1.26.4 to v1.27.2

---

## References:

- [Kubernetes documentation: Upgrading kubeadm clusters](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)
- [Install Kubernetes (kubectl, kubeadm, kubelet) on debian stretch](https://stackoverflow.com/a/52533972)
- [Kind: Quick-start ~ Create multi node cluster](https://kind.sigs.k8s.io/docs/user/quick-start/#advanced)
- [Kindnet: Kind CNI Plugin](https://github.com/aojea/kindnet) 
