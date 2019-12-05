---
layout: post
title: "Outreachy - Week 01, Day 02!"
description: "The Progress report of Day 2 of work for Outreachy Program."
category: Outreachy
tags: [Outreachy, GNOME, GTranslator, Internship, Daily-Progress]
comments: false
---

December 04, 2019

**Task for the week:**

- Try to replicate the [gnome-builder](https://gitlab.gnome.org/GNOME/gnome-builder/) "search and replace bar" widget (just the wire-frame) in the Gtranslator project.

**Progress of the day:**

- Today was a slightly more productive day. I was able to fix yesterday's *[build-environment errors](https://priyankasaggu11929.github.io/outreachy/2019/12/03/Outreachy-Day-1.html)* early in the morning itself, so the rest of the day was saved from all that hassle and I was free to tweak the source-code now. What I learned from all that environment-related mess (I created yesterday) is:
   
  + I should have stopped yesterday early enough only. Because what I needed most was a fresh approach today. The reason why I am stating it here is that *repeating a wrong approach over and over again just results in nothing*. Yesterday, I was just repeating the same process almost for the whole day. I was exhausted enough after staring at the screen (at those endless build reports ending just into failure every time) that my mind had stopped working (almost) entirely. I was not able to figure out my smallest mistakes even. For instance, for the whole time, I was cloning `gnome-builder` source code from *[salsa.debian.org](https://salsa.debian.org/gnome-team/gnome-builder)* instead of doing it from *[gitlab.gnome.org](https://gitlab.gnome.org/GNOME/gnome-builder/)* and was wondering why it didn't work for me 🤦. (See, this happens when one over-exerts something).
  
  + I should ask more frequently when I am sure by myself that I have tried enough solutions for the problem and none of them worked for me. Because even the smallest leads from the mentor accelerate the whole process by 100x. For instance, I informed danigm last night that so-so was the scenario and I was not able to fix it. And he, telling me that I should try building it from the last-stable branch, just cleared everything. Even that was another piece of learning for the day and I felt much more confident while solving the further errors I had during the process. (Yes, I was able to build both the projects from the master branch as well later on. 😄)
  
  + And lastly admitting early enough that a solution which seems wrong could be wrong, creates more chance of leading quickly towards the alternative right solutions.
- The next step for today was to try adding "search and replace bar" related snippets of code from the `gnome-builder` project into `gtranslator`. And in no time, I got another error for the missing run-time dependency '[libdazzle-1.0](https://gitlab.gnome.org/GNOME/libdazzle)`. This time I knew what this dependency was for but again had no idea how to add it inside the project.

- After reading for a while, I realized that most of these run-time dependencies come packed inside the available `runtimes` itself. So, the only criteria for deciding a `runtime` for a project is evaluating the kind of dependencies, the project is going to use and then analyzing which `runtime` comes bundled with them.

- But again, (AFAIR but I might be wrong also) the `libdazzle-1.0` is not bundled in any of the available runtimes. So, the next step was to search for how these unbundled dependencies could be added to a project. I didn't find any good documentation for the same, therefore, the last step was to read the source-code of `gnome-builder` itself and check how `libdazzle-1.0` was added there (the best part was that `gnome-builder` is the only project that implements it primarily, so I was staright away to the solution). After an hour or so, I finally find out how it was done. And voila, I was one more step ahead in the process 🙌. 
The solution was:

```  
  # Dependencies #
  . . .

  dependency('libdazzle-1.0', version: '>= 3.33.90')
  . . .
```
*-- meson.build*

```
 "modules" : [

        . . .

        {
            "name" : "libdazzle",
            "config-opts" : [
                "--libdir=/app/lib",
                "--buildtype=release"
            ],
            "buildsystem" : "meson",
            "builddir" : true,
            "cleanup" : [
                "/bin"
            ],
            "sources" : [
                {
                    "type" : "git",
                    "url" : "https://gitlab.gnome.org/GNOME/libdazzle.git",
                    "branch" : "libdazzle-3-34"
                }
            ]
        },

       . . .
] 

```
*--build-aux/flatpak/org.gnome.Gtranslator.json*

- Besides, I wrote a simple *python script* to quickly create my daily Outreachy post templates (same as today's post) so that I could essentially cut out the time to prep a markdown template every day, *just* to start the post. Hopefully, it will save me lots of time which unneccesarily goes into thinking about "how to start" and "how to proceed".

That's all for today. 

Till tomorrow. o/


