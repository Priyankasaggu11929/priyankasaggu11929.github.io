---
layout: post
title: "[node-reviewer-group] Tasks progress!"
description: "A short post around the task progress from kubernetes node-reviewer-group mentorship program tasks!"
category: Kubernetes-mentorship
tags: [Kubernetes]
comments: false
---

July 30, 2020

Some quick logs for the progress, solutions & resources around the first set of *node-reviewer-group* mentorship program tasks.

---

- [X] **Task #1 : Compile kubelet**
    - See tips in the root Makefile
 
***Solution:***

- Clone `kubernetes/kubernetes` github repository. Use `--depth` flag for quick light download.
- Change directory to the cloned repository.
- Build/Compile the go targets for kubelet.

```bash
$ git clone --depth=1 https://github.com/kubernetes/kubernetes.git
$ cd kubernetes
$ sudo make kubelet 
```
---
 
- [X] **Task #2 : Run a single unit test**
    - See tips in the root Makefile

***Solution:***

- Inside the same `kubernetes` directory, first setup `Bazel` for testing.
- Once Bazel is setup, check whether the bazel version is the one required to run tests for the packages present in cloned kubernetes repo.
- Let's take an example case where we are trying to run test cases for `pkg/scheduler` package.
- This command, `bazel test //pkg/scheduler...` will run all tests under the scheduler package.
- But as asked in the task, we need to run a single unit test under a specific package. So, this command `bazel test //pkg/scheduler/apis/config/v1beta1:go_default_test` will run a single specific testcase.

```bash
# SETTING UP BAZEL

$ echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
$curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -
$ sudo apt-get update && sudo apt-get install bazel
$ sudo apt-get install --only-upgrade bazel
```

**(RUNNING ALL TEST CASES UNDER A PACKAGE)**

```bash
$ bazel test //pkg/scheduler...

## OUTPUT

...
module golang.org/x/tools@latest found (v0.0.0-20200729194436-6467de6f59a7), but does not contain package golang.org/x/tools/internal/lsp/baz
gazelle: finding module path for import golang.org/x/tools/internal/lsp/signature: exit status 1: go: finding module for package golang.org/x/tools/internal/lsp/signature
module golang.org/x/tools@latest found (v0.0.0-20200729194436-6467de6f59a7), but does not contain package golang.org/x/tools/internal/lsp/signature
INFO: Analyzed 185 targets (216 packages loaded, 1159 targets configured).
INFO: Found 144 targets and 41 test targets...
INFO: Elapsed time: 103.034s, Critical Path: 42.76s
INFO: 448 processes: 448 linux-sandbox.
INFO: Build completed successfully, 527 total actions
//pkg/scheduler/apis/config/v1:go_default_test                  (cached) PASSED in 0.1s
//pkg/scheduler/apis/config/v1beta1:go_default_test             (cached) PASSED in 0.1s
//pkg/scheduler:go_default_test                                          PASSED in 18.7s
//pkg/scheduler/algorithmprovider:go_default_test                        PASSED in 0.2s
//pkg/scheduler/apis/config:go_default_test                              PASSED in 0.2s
...
//pkg/scheduler/profile:go_default_test                                  PASSED in 0.2s
//pkg/scheduler/util:go_default_test                                     PASSED in 0.4s

Executed 39 out of 41 tests: 41 tests pass.
```

**(RUNNING SINGLE CASE UNDER A PACKAGE)**

```bash
$ bazel test //pkg/scheduler/apis/config/v1beta1:go_default_test

## OUTPUT

...
gazelle: finding module path for import golang.org/x/tools/internal/lsp/baz: exit status 1: go: finding module for package golang.org/x/tools/internal/lsp/baz
module golang.org/x/tools@latest found (v0.0.0-20200729194436-6467de6f59a7), but does not contain package golang.org/x/tools/internal/lsp/baz
gazelle: finding module path for import golang.org/x/tools/internal/lsp/signature: exit status 1: go: finding module for package golang.org/x/tools/internal/lsp/signature
module golang.org/x/tools@latest found (v0.0.0-20200729194436-6467de6f59a7), but does not contain package golang.org/x/tools/internal/lsp/signature
INFO: Analyzed target //pkg/scheduler/apis/config/v1:go_default_test (1 packages loaded, 9 targets configured).
INFO: Found 1 test target...
Target //pkg/scheduler/apis/config/v1:go_default_test up-to-date:
  bazel-bin/pkg/scheduler/apis/config/v1/linux_amd64_stripped/go_default_test
INFO: Elapsed time: 2.368s, Critical Path: 1.78s
INFO: 6 processes: 6 linux-sandbox.
INFO: Build completed successfully, 9 total actions
//pkg/scheduler/apis/config/v1:go_default_test                           PASSED in 0.1s

Executed 1 out of 1 test: 1 test passes.
```

---

- [X] **Task #5 : Using local-up-cluster script**
    - https://github.com/kubernetes/community/blob/master/contributors/devel/running-locally.md#starting-the-cluster
    
- This requires setting up the following beforehand.
    - Docker
    - etcd
    - go
    - OpenSSL
    - CFSSL
- For installing a local copy of `etcd`, use the following set of commands.

    ```bash
    cd $working_dir/kubernetes
    
    # Installs in ./third_party/etcd
    hack/install-etcd.sh

    # Add to PATH
    echo export PATH="\$PATH:$working_dir/kubernetes/third_party/etcd" >> ~/.profile
    ```
- You are required to add the `etcd` PATH to your system's `PATH` variable first & then to the `secure\_path` for sudo. Once done, reboot your system to reflect the changes.

    ```bash
    $ sudo su
    $ sudo echo export PATH="\$PATH:$working_dir/kubernetes/third_party/etcd" >> ~/.profile
    $ sudo echo export PATH="\$PATH:$working_dir/kubernetes/third_party/etcd" >> /root/.profile

    $ sudo su -
    $ visudo

    # Now the secure path should look like this:

    Defaults
    secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$working_dir/kubernetes/third_party/etcd

    # Reboot your host:

   $ sudo shutdown -r
   ```

- Verify your etcd version, once finished rebooting.

   ```bash
   $ etcd --version
   $ sudo etcd --version
   ```
- In a separate tab of your terminal, run the following command. This will build and start a lightweight local cluster, consisting of a master and a single node. Press Control+C to shut it down.

    ```bash
    sudo ./hack/local-up-cluster.sh
   
    # OUTPUT
   
    ...
    Create default storage class for 
    storageclass.storage.k8s.io/standard created
    Local Kubernetes cluster is running. Press Ctrl-C to shut it down.

    Logs:
       /tmp/kube-apiserver.log
       /tmp/kube-controller-manager.log
  
       /tmp/kube-proxy.log
       /tmp/kube-scheduler.log
       /tmp/kubelet.log

    To start using your cluster, you can open up another terminal/tab and run:

    export KUBECONFIG=/var/run/kubernetes/admin.kubeconfig
    cluster/kubectl.sh

    Alternatively, you can write to the default kubeconfig:

    export KUBERNETES_PROVIDER=local

    cluster/kubectl.sh config set-cluster local --server=https://localhost:6443 --certificate-authority=/var/run/kubernetes/server-ca.crt
    cluster/kubectl.sh config set-credentials myself --client-key=/var/run/kubernetes/client-admin.key --client-certificate=/var/run/kubernetes/client-admin.crt
    cluster/kubectl.sh config set-context local --cluster=local --user=myself
    cluster/kubectl.sh config use-context local
    cluster/kubectl.sh
    ```
    
 - Keep the above cluster running. From another terminal session, You can now use any of the cluster/kubectl.sh commands to interact with your local setup.

   ```bash
   ./cluster/kubectl.sh get pods
   ./cluster/kubectl.sh get services
   ./cluster/kubectl.sh get replicationcontrollers
   ./cluster/kubectl.sh run my-nginx --image=nginx --port=80
   ./cluster/kubectl.sh create -f test/fixtures/doc-yaml/user-guide/pod.yaml
   ```
---

**PENDING TASKS**
    
- [ ] Task #3 : Explore update/verify scripts
    - hack/update-gofmt.sh + hack/verify-gofmt.sh
    - hack/update-bazel.sh + hack/verify-bazel.sh
- [ ] Task #4 : Explore dependencies
    - hack/pin-dependency.sh + hack/update-vendor.sh
    
 ---
 
 **REFERENCES**
 
 - [1] [sig-node mentoring](https://hackmd.io/@XYdYH0X5SYC3DUYFF5Wylg/SyYoo-U1w)
 - [2] [Getting started locally](https://github.com/kubernetes/community/blob/master/contributors/devel/running-locally.md#starting-the-cluster)
 - [3] [Installing Bazel on Ubuntu](https://docs.bazel.build/versions/1.0.0/install-ubuntu.html)
 - [4] [Setup guide for Kubernetes developers](https://developer.ibm.com/articles/setup-guide-for-kubernetes-developers/)
 - [5] [Build and test with Bazel](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-testing/bazel.md)
 - [6] [Tip: User `--test_filter`](https://www.google.com/search?q=bazel+golang+test_filter)
 - [7] [Building Go Applications with Bazel](https://www.google.com/search?q=bazel+golang+test_filter)
