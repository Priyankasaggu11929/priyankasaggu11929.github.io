---
layout: post
title: "What is Container Runtime Interface (CRI)"
description: ""
category: 
tags: []
comments: false
---


Bite size notes for me!

#### What is Container Runtime?

A software that is responsible for running containers.
Examples - CRI-o, Containerd, Docker

#### What is CRI?

stands for Container Runtime Interface

API for container runtimes to integrate with kubelet

A gRPC API that kubelet uses to communicate with container runtimes (like CRI-O, Containerd, Docker)

CRI — (image service + runtime service)

- image service – manage images i.e, pulling, listing & removing images

- runtime service – manage lifecycle of pods and containers (i.e., create, start, stop, and remove)

