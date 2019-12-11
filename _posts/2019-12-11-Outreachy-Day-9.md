---
layout: post
title: "Outreachy - Week 02, Day 03!"
description: "The Progress report of Day 9 of work for Outreachy Program."
category: Outreachy
tags: [Outreachy, GNOME, GTranslator, Internship, Daily-Progress]
comments: false
---

December 11, 2019

**Task for the week:**

- Try to replicate the gnome-builder “search and replace bar” widget (just the wire-frame) in the Gtranslator project.
  - [sub-task] First try doing the above task in a seperate simple application.

**Progress of the day:**

- It was again a day full of learning new things. Although, there is no tangible progress even now but certainly I'm taking a step or two ahead everyday.

- Today, I learnt a (considerably) accurate way of isolating build environments of the development and installed instances of a same application. Now, rather than changing the `app-id` (which I realised is not the recommended way because of the `file naming convention` across a project. Some files such as .desktop files, export files etc. includes the `app-id` in their names itself) but by adding some special command line arguments in the flatpak manifests i.e `"x-run-args" : ["--standalone", "-vvvv"]`. 
 
  - Adding the `--standalone` argument will make the development application run with `G_APPLICATION_NON_UNIQUE` flag. That means the application is isolated at most part. 

  - The only thing that require more tweaking for isolation is the *"name of the application on the session bus"*. It is the case when the application is involved in IPC (<strike>which is the scenario in my case, so, it didn't help me much but I learnt something new and important.</strike> I managed to get the changes reflected in the build run. Yay \o/)

(you might need to read some of the previous day's blogs to understand the context of my above point.)

- I have started creating `search-and-replace-bar` widget in the example application. Hope, I will soon get some considerable progress in the coming day.

- Reading [blogs from the Builder-developers](https://blogs.gnome.org/chergert/category/builder/) actually made me realise how powerful and feature-packed this IDE is.
 
  - I learnt that Builder-IDE has support for a Designer, here Glade 3. That means it is easier to see widgets created using composition. (<strike>For all these times, I was struggling so hard to tweak even simple things in the ui file without this designer. Finally I have it!</strike> I am still struggling because it is throwing errors.)

  ![glade-error](/assets/glade-error.png)

  - I can split files into multiple separate workspaces that means my long-standing issue of handling multiple files from different projects at the same time is solved very beautifully now. Definitely I've much more to learn about gnome-builder even now. But I'm starting liking it now.

That's all for the day!


Till tomorrow. o/

