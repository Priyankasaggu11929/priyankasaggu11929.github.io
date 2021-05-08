---
layout: post
title: "[Python for DevOps] Infrastructure testing using `pytest` plugin `Testinfra`!"
description: "This post contain notes from Chapter-8 'Pytest for DevOps' from the book, Python for DevOps!"
category: learning-python
tags: [DevOps, Python, Notes]
comments: false
---

August 10, 2020

In the [last post](https://priyankasaggu11929.github.io/learning-python/2020/08/10/pfd-pytest-for-devops.html), we discussed about using `pytest` module for writing traditional software tests.

Here, we will be expanding the same for performing *Infrastructure testing* using `pytest` module.
<!-- break -->

*(Note: The notes below are the direct excerpts from the book, [Python For DevOps](https://learning.oreilly.com/library/view/python-for-devops/9781492057680/), compiled for the purpose of learning & memory.)*

---

### Infrastructure Testing (*my favorite part :D*)

[Testinfra project](https://testinfra.readthedocs.io/en/latest/) is a `pytest` plug-in for infrastructure testing that relies heavily on fixtures and allows you to write Python tests as if testing code.

> The way we explain infrastructure testing is by asking a question: ***How can you tell that the deployment was successful?***
>
> Most of the time, this means some manual checks, such as loading a website or looking at processes, which is insufficient; it is error-prone and can get tedious if the system is significant.

- The `TestInfra` project has all kinds of fixtures to test a system efficiently, and it includes a complete set of backends to connect to servers, regardless of their deployment type: Ansible, Docker, SSH, and Kubernetes are some of the supported connections. By supporting many different connection backends, you can execute the same set of tests regardless of infrastructure changes.

> **System validation** can happen at different levels (with monitoring and alert systems) and at different stages in the life cycle of an application, such as during pre-deployment, at runtime, or during deployment. An application that Alfredo recently put into production needed to handle client connections gracefully without any disruption, even when restarted. To sustain traffic, the application is load balanced: when the system is under heavy loads, new connections get sent to other servers with a lighter load.
>
> When a new release gets deployed, the application has to be restarted. Restarting means that clients experience an odd behavior at best, or a very broken experience at the worst. To avoid this, the restart process waits for all client connections to terminate, the system refuses new connections, allowing it to finish work from existing clients, and the rest of the system picks up the work. When no connections are active, the deployment continues and stops services to get the newer code in.
> There is validation at every step of the way: 
> - before the deployment to tell the balancer to stop sending new clients 
> - and later, verifying that no new clients are active. 
>
> If that workflow converts to a test, the title could be something like: **make sure that no clients are currently running**. 
>
> Once the new code is in, 
> - another validation step checks whether the balancer has acknowledged that the server is ready to produce work once again. 
> - Another test here could be: balancer has server as active. 
> - Finally, it makes sure that the server is receiving new client connections—yet another test to write!
>
> Throughout these steps, verification is in place, and tests can be written to verify this type of workflow.

---

- Create a new virtual environment `validation`, and install pytest.

```bash
$ python3 -m venv validation
$ source testing/bin/activate
(validation) $ pip install pytest
```
- Install `testinfra`, ensuring that version 2.1.0 is used.

```bash
(validation) $ pip install "testinfra==2.1.0"
```

- Because different backend connection types exist, when the connection is not specified directly, Testinfra defaults to certain ones. It is better to be explicit about the connection type and define it in the command line.

- These are all the connection types that Testinfra supports:
    - local
    - Paramiko (an SSH implementation in Python)
    - Docker
    - SSH
    - Salt
    - Ansible
    - Kubernetes (via kubectl)
    - WinRM
    - LXC

- A `testinfra` section appears in the help menu with some context on the flags that are provided. This is a neat feature from `pytest` and its integration with Testinfra. The help for both projects comes from the same command:

```bash
(validation) $ pytest --help
...

testinfra:
  --connection=CONNECTION
                        Remote connection backend (paramiko, ssh, safe-ssh,
                        salt, docker, ansible)
  --hosts=HOSTS         Hosts list (comma separated)
  --ssh-config=SSH_CONFIG
                        SSH config file
  --ssh-identity-file=SSH_IDENTITY_FILE
                        SSH identify file
  --sudo                Use sudo
  --sudo-user=SUDO_USER
                        sudo user
  --ansible-inventory=ANSIBLE_INVENTORY
                        Ansible inventory file
  --nagios              Nagios plugin
```

Let's try to understand the infrastructure testing using `pytest` with an example.

- Say, there are two servers up and running. To demonstrate the connection options, let’s check if they are running CentOS 7 by poking inside the `/etc/os-release` file. This is how the test function looks (saved as test_remote.py).

```python
def test_release_file(host):
    release_file = host.file("/etc/os-release")
    assert release_file.contains('CentOS')
    assert release_file.contains('VERSION="7 (Core)"')
```

- It is a single test function that accepts the `host` fixture, which runs against all the nodes specified.
    - The `--hosts` flag accepts a list of hosts with a connection scheme (*SSH would use `ssh://hostname` for example*), and some other variations using globbing are allowed.

- If we're testing against more than a couple of remote servers at a time, passing the hosts on the command line becomes cumbersome. This is how it would look to test against two servers using SSH

```bash
(validation) $ pytest -v --hosts='ssh://node1,ssh://node2' test_remote.py

============================= test session starts =============================
platform linux -- Python 3.6.8, pytest-4.4.1, py-1.8.0, pluggy-0.9.0
cachedir: .pytest_cache
rootdir: /home/alfredo/python/python-devops/samples/chapter16
plugins: testinfra-3.0.0, xdist-1.28.0, forked-1.0.2
collected 2 items

test_remote.py::test_release_file[ssh://node1] PASSED                   [ 50%]
test_remote.py::test_release_file[ssh://node2] PASSED                   [100%]

========================== 2 passed in 3.82 seconds ===========================
```

- The increased verbosity (with the -v flag) shows that Testinfra is executing the one test function in the two remote servers specified in the invocation.

> When setting up the hosts, it is important to have a passwordless connection. There shouldn’t be any password prompts, and if using SSH, a key-based configuration should be used.

---

Testinfra can consume an **SSH configuration file** to determine what hosts to connect to. For the previous test run, Vagrant was used, which created these servers with special keys and connection settings. Vagrant can generate an ad-hoc SSH config file for the servers it has created.

```bash
(validation) $ vagrant ssh-config

Host node1
  HostName 127.0.0.1
  User vagrant
  Port 2200
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile /home/alfredo/.vagrant.d/insecure_private_key
  IdentitiesOnly yes
  LogLevel FATAL

Host node2
  HostName 127.0.0.1
  User vagrant
  Port 2222
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile /home/alfredo/.vagrant.d/insecure_private_key
  IdentitiesOnly yes
  LogLevel FATAL
```

- Exporting the contents of the above output to a file and then passing that to `Testinfra` as a flag offers greater flexibility if using more than one host.

```bash
(validation) $ vagrant ssh-config > ssh-config
(validation) $ pytest --hosts=default --ssh-config=ssh-config test_remote.py
```

- Using `--hosts=default` avoids having to specify them directly in the command line, and the engine feeds from the SSH configuration. 

---

*Ansible* is another option if the nodes are local, SSH, or Docker containers. The test setup can benefit from using an inventory of hosts (much like the SSH config), which can group the hosts into different sections. The host groups can also be specified so that you can single out hosts to test against, instead of executing against all.

- For node1 and node2 used in the previous example, this is how the inventory file is defined (and saved as `hosts` file):

```
[all]
node1
node2
```

- If executing against all of them, the command changes to:

```bash
$ pytest --connection=ansible --ansible-inventory=hosts test_remote.py
```

- If defining other hosts in the inventory that need an exclusion, a group can be specified as well. Assuming that both nodes are web servers and are in the nginx group, this command would run the tests on only that one group:

```bash
$ pytest --hosts='ansible://nginx' --connection=ansible \
  --ansible-inventory=hosts test_remote.py
```

> A lot of system commands require superuser privileges. To allow escalation of privileges, Testinfra allows specifying `--sudo` or `--sudo-user`. 
>
> The `--sudo` flag makes the engine use sudo when executing the commands, while the `--sudo-user` command allows running with higher privileges as a different user.The fixture can be used directly as well.

---

#### Features and Special Fixtures

> So far, the host fixture is the only one used in examples to check for a file and its contents. However, this is deceptive. The host fixture is an all-included fixture; it contains all the other powerful fixtures that Testinfra provides. This means that the example has already used the host.file, which has lots of extras packed in it. It is also possible to use the fixture directly.

```python
In [1]: import testinfra

In [2]: host = testinfra.get_host('local://')

In [3]: node_file = host.file('/tmp')

In [4]: node_file.is_directory
Out[4]: True

In [5]: node_file.user
Out[5]: 'root'
```

- The all-in-one `host` fixture makes use of the extensive API from Testinfra, which loads everything for each host it connects to.

(*Check all the attributes available [here](https://testinfra.readthedocs.io/en/latest/modules.html).*)

- The below are some of the most used ones.
    - `host.ansible`: Provides full access to any of the Ansible properties at runtime, such as hosts, inventory, and vars.
    - `host.addr`: Network utilities, like checks for IPV4 and IPV6, is host reachable, is host resolvable.
    - `host.docker`: Proxy to the Docker API, allows interacting with containers, and checks if they are running.
    - `host.interface`: Helpers for inspecting addresses from a given interface.
    - `host.iptables`: Helpers for verifying firewall rules as seen by host.iptables.
    - `host.mount_point`: Check mounts, filesystem types as they exist in paths, and mount options.
    - `host.package`: Very useful to query if a package is installed and at what version.
    - `host.process`: Check for running processes.
    - `host.sudo`: Allows you to execute commands with host.sudo or as a different user.
    - `host.system_info`: All kinds of system metadata, such as distribution version, release, and codename.
    - `host.check_output`: Runs a system command, checks its output if runs successfully, and can be used in combination with `host.sudo`.
    - `host.run`: Runs a command, allows you to check the return code, `host.stderr`, and `host.stdout`.
    - `host.run_expect`: Verifies that the return code is as expected.

---

### Examples

- A frictionless way to start developing system validation tests is to do so while creating the actual deployment. Somewhat similar to *Test Driven Development* (TDD), any progress warrants a new test.

- Here, a web server needs to be installed and configured to run on port 80 to serve a static landing page.

- With a *vanilla* Ubuntu server, start by installing the Nginx package:

```bash
$ sudo apt install nginx
```
		
- Create a new test file called `test_webserver.py` for adding new tests after making progress. After Nginx installs, let’s create another test:
    
```python
def test_nginx_is_installed(host):
	assert host.package('nginx').is_installed
```
- Reduce the verbosity in `pytest` output with the `-q` flag to concentrate on failures. The remote server is called `node4` and SSH is used to connect to it. This is the command to run the first test.

```bash
(validate) $ pytest -q --hosts='ssh://node4' test_webserver.py
.
1 passed in 1.44 seconds

## YOU COULD TEST THE SAME ON LOCAL MACHINE WITH THE FOLLOWING COMMAND:

(validate) $ pytest -q test_webserver.py
.                                                                          [100%]
1 passed in 0.20s
```

- The web server needs to be up and running, so a new test is added to verify that behavior.

```python
def test_nginx_is_running(host):
    assert host.service('nginx').is_running
```

- The web server should be serving a static landing page on `port 80`. Adding another test (in `test_webserver.py`) to verify the port is the next step.
    - This test is more involved and needs attention to some details.
    -  It opts to check for TCP connections on port 80 on any IP in the server. 

```python
def test_nginx_listens_on_port_80(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening
```

- Since there isn’t a built-in fixture to handle HTTP requests to an address, the final test uses the wget utility to retrieve the contents of the running website and make assertions on the output to ensure that the static site renders.

```python
def test_get_content_from_site(host):
    output = host.check_output('wget -qO- 0.0.0.0:80')
    assert 'Welcome to nginx' in output
```

- So, the final run will give the output like:

```bash
(validate) $ pytest -v --hosts='ssh://node4' test_webserver.py

================================ test session starts ================================
platform linux -- Python 3.8.2, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/priyankasaggu119/Desktop/.myhome/python-study
plugins: testinfra-2.1.0
collected 4 items                                                                   

test_webserver.py::test_nginx_is_installed[local] PASSED                      [ 25%]
test_webserver.py::test_nginx_is_running[local] PASSED                        [ 50%]
test_webserver.py::test_nginx_listens_on_port_80[local] PASSED                [ 75%]
test_webserver.py::test_get_content_from_site[local] PASSED                   [100%]

================================= 4 passed in 0.22s =================================

```

### Testing Jupyter Notebooks with pytest [PENDING]

One easy way to introduce big problems into your company is to forget about applying software engineering best practices when it comes to data science and machine learning. One way to fix this is to use the `nbval` (notebook-validation) plug-in for `pytest` that allows you to test your notebooks. Take a look at this Makefile:

```makefile
setup:
    python3 -m venv ~/.myrepo

install:
    pip install -r requirements.txt

test:
    python -m pytest -vv --cov=myrepolib tests/*.py
    python -m pytest --nbval notebook.ipynb

lint:
    pylint --disable=R,C myrepolib cli web

all: install lint test
```

- The key item is the `--nbval` flag that also allows the notebook in the repo to be tested by the build server.
