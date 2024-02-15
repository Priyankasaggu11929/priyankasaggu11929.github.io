---
layout: post
title: "What is OSTree?"
description: ""
category: 
tags: []
comments: false
---


Bite size notes for me!

#### What is OSTree?

upgrade system for linux-based operating systems

performs atomic upgrades of complete filesystem trees (sounds like transactional updates to me? Is that's why bootc is called transactional updates something?)

operates in userspace (in oppose to kernel?), will work on top of any linux filesystem

#### OSTree — git for operating system binaries?

underlying architecture could be summarized as — git for operating system binaries

at its core, it is a git-like content-addressed object store with branches or refs, to track meaningful filesystem trees within the store

similar to git, I can check out or commit to these branches (but how? let's see if I can find out below or later?)

#### OSTree — what other than the git-like architecture?

layered on top of the underlying git-like architecture is
- bootloader configuration
- management of `/etc`
- and, other functions to perform an upgrade beyond just replicating files

I don't understand the following bit, but let's see maybe with more work, I can start making sense of it
(I've my vague idea of it, but let's see. for record, I am imagining it as [transactional-update command in SLE micro](https://documentation.suse.com/sle-micro/5.3/html/SLE-Micro-all/sec-transactional-udate.html#sec-command-list))

> You can use OSTree standalone in the pure replication model,
> but another approach is to add a package manager on top,
> thus creating a hybrid tree/package system.


And before I move forward, I just learnt the project is now known as "[libostree](https://ostreedev.github.io/ostree/#libostree)" 

Ok, I'm still trying to understand whether it's just a name change or other things have also changed

Before I move ahead, I'm gonna run `zypper search libostree` in my openSUSE Tumbleweed VM to check if we have this packaged.

And yes, we have it (them?) !!! (so, I need to now understand how we're already using OSTree or libostree capabilities)

And I've some of these installed too (well, I just recalled that is because I was trying to build the bootc project few hours back and libostree was a dependency, [which makes total sense now!](https://youtu.be/QaKl5z6dFlM?feature=shared&t=653))

```
> zypper search libostree
Loading repository data...
Reading installed packages...

S  | Name            | Summary                                                | Type
---+-----------------+--------------------------------------------------------+--------
   | libostree       | Git for operating system binaries                      | package
i  | libostree-1-1   | Git for operating system binaries                      | package
i+ | libostree-devel | Git for operating system binaries -- Development files | package
   | libostree-grub2 | GRUB2 integration for OSTree                           | package
```

well, I had to go ahead and install the one that wasn't already installed to get the `ostree` binary.

So, `zypper in libostree` and then `rpm -ql libostree` to check what all I got with this package
(lots! and for now, I saw `/usr/bin/ostree` and so, let's move on with the "hello world" example)

I'm doing the following in order (basically copy/paste from ["Hello World example"](https://ostreedev.github.io/ostree/introduction/#hello-world-example))

```
> ostree --repo=repo init

The repo folder indeed looks like a git-like structure

> ls -l repo
total 4
-rw-r--r-- 1 dos dos 32 Feb 15 17:38 config
drwxr-xr-x 1 dos dos  0 Feb 15 17:38 extensions
drwxr-xr-x 1 dos dos  0 Feb 15 17:38 objects
drwxr-xr-x 1 dos dos 38 Feb 15 17:38 refs
drwxr-xr-x 1 dos dos  0 Feb 15 17:38 state
drwxr-xr-x 1 dos dos 10 Feb 15 17:38 tmp
```

I got over enthusiastic and tried to play around with other subcommands of ostree.
Collected myself (because not much, actally hardly anything make sense) and back to hello world!

```
> mkdir tree

> echo "Hello World!" > tree/hello.txt

> ostree --repo=repo commit --branch=foo tree/
e7aed806fd51630b7cc52f9bfd3ff441c20a8bf916f97d9dd3c654b486661577
```
Docs say above commands created a branch "foo" in the "repo" (empty repo we initiated in the very first step)

indeed it did!

```
> ostree --repo=repo refs
foo

> ostree --repo=repo ls foo
d00755 1000 1000      0 /
-00644 1000 1000     13 /hello.txt

> ostree --repo=repo checkout foo tree-checkout/

> cat tree-checkout/hello.txt 
Hello World!


```

but I went and ran a few more things in the repo folder too, to check where all stuff appeared.

```
> ls repo/refs/heads/
foo

> cat repo/refs/heads/foo 
e7aed806fd51630b7cc52f9bfd3ff441c20a8bf916f97d9dd3c654b486661577

> ls repo/objects/
27  66  79  e7

> cat repo/objects/27/67351174f75f3ae221f7c7a48bb0fdd25ee00147c10d6817f5ef61922d327b.dirtree 
hello.txtfYڅB-Y%o.���gL�4�x�o���<�

> cat repo/objects/66/59da85422d59256f2e16c3ebde1c674ced9934d978e6826fe99fc413db3cb0.file
Hello World!


```
