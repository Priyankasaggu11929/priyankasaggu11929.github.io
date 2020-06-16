---
layout: post
title: "Writing containers from scratch in Go!"
description: "This is my notes from the DockerCon'2017 talk on writing containers from scratch by Liz Rice."
category: Containerization, Docker, Go
tags: [Docker, Containerization, Go]
comments: false
---

June 16, 2020

Okay, finally I'm here writing something technical. I'm still not sure what's gonna be the flow but I'm keeping my hopes high (*or otherwise I'll strike it once I'm done XD*).

Actually this post is gonna be my *talk-notes* for the *Liz Rice's* talk *[What Have Namespaces Done for You Lately?](https://www.youtube.com/watch?v=MHv6cWjvQjM)* So, everything written later in the post is entirelly credited to *[Liz Rice](https://www.lizrice.com/)* who in-turn thanks *[Julian Friedman](https://twitter.com/doctor_julz)* for the talk idea & the code snippets used inside.

Let's get started now!

---

Before jumping into writing a container of our own from scratch, the first thing is to understand **what actually a container is**?

*From my understanding so far, a container simply is a means for process isolation. I'm sure it is in no way a complete definition but definitely a broader idea. So, what completes the definition, is knowing about the following 3 things which makes up the majority of the container.*

- *Namespaces - What your container can see!*
- *Control Groups (cgroups) - What your container can use!*
- *layered filesystem - The home for the above two, to do all their magic.*

![What-is-container](assets/container.jpeg)

Ok, now that our base idea is ready, we know what elements we need to implement in order to write our container from scratch.

So, it's a good time to jump into the actual go implementation now. 

```go
package main

import (
	"fmt"
	"os"
	"os/exec"
	"syscall"
)

func main() {
	switch os.Args[1] {
	case "run":
		parent()
	case "child":
		child()
	default:
		panic("Something else!")
	}
}

func parent() {
	cmd := exec.Command("/proc/self/exe", append([]string{"child"}, os.Args[2:]...)...)
	cmd.SysProcAttr = &syscall.SysProcAttr{
		Cloneflags: syscall.CLONE_NEWUTS | syscall.CLONE_NEWPID | syscall.CLONE_NEWNS,
	}
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		fmt.Println("ERROR", err)
		os.Exit(1)
	}
}

func child() {
	must(syscall.Mount("rootfs", "rootfs", "", syscall.MS_BIND, ""))
	must(os.MkdirAll("rootfs/oldrootfs", 0700))
	must(syscall.PivotRoot("rootfs", "rootfs/oldrootfs"))
	must(os.Chdir("/"))

	cmd := exec.Command(os.Args[2], os.Args[3:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		fmt.Println("ERROR", err)
		os.Exit(1)
	}
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}
```


---

### REFERENCES:

- [1] [Build Your Own Container Using Less than 100 Lines of Go](https://www.infoq.com/articles/build-a-container-golang/)
- [2] [Source Code from Liz Rice's talk](https://github.com/lizrice/containers-from-scratch/blob/master/main.go)
- [3] [Source Code from Julian Friedman's article](https://gist.github.com/christophberger/58505418133d474486a88f958d8ea14b)
