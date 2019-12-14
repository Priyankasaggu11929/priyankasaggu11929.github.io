---
layout: post
title: "Outreachy week-2 progress report!"
description: "This is the compilation of the project progress during week-2 of outreachy internship."
category: Outreachy
tags: [Outreachy, GNOME, GTranslator, Internship, Weekly-Progress]
comments: false
---

December 15, 2019

**Task for the week:**

- Try to replicate the gnome-builder “search and replace bar” widget (just the wire-frame) in the Gtranslator project.
  - [sub-task] First try doing the above task in a seperate simple application.

**Summary of the week:**

It was a really productive week. I am almost done with the current tasks. I've finished replicating the wire-frame of gnome-builder's `search-and-replace-bar` widget into the *[libdazzle-example](https://gitlab.gnome.org/priyankasaggu119/example)* application (although, it's a complete mess piece of code right now, that I'll refactor once I see it is *actually* working). There are a couple (or maybe a couple more) of final nitpicks to do to actually mark these as finished. 

At the moment, I *am* far more comfortable with the project. Nothing seems *really* alien-sih now, rather most of the stuffs (from the project) looks quite familier (and imparts somewhat proper sense).

### Compiling below each day's progress in brief:

[Day 01](https://priyankasaggu11929.github.io/outreachy/2019/12/09/Outreachy-Day-7.html): 
- Finished setting up and building the [libdazzle’s example application](https://gitlab.gnome.org/GNOME/libdazzle/blob/master/examples/app).

[Day 02](https://priyankasaggu11929.github.io/outreachy/2019/12/10/Outreachy-Day-8.html):
- Had my first weekly-meeting with [danigm](http://danigm.net). Discussed various standing doubts. 
- Then later in the day, attended the first outreachy zulip chat conversation.

[Day 03](https://priyankasaggu11929.github.io/outreachy/2019/12/11/Outreachy-Day-9.html): 
- Was able to build and isolate the `gnome-builder`'s development environment properly. 
- Read a couple of blogs from the [gnome-builder developers](https://blogs.gnome.org/chergert/category/builder/). Thus, explored a couple of new (then unknown) features of the Builder-IDE.
- Later, also started replicating the `search-and-replace-bar` widget in the example application.

[Day 04](https://priyankasaggu11929.github.io/outreachy/2019/12/13/Outreachy-Day-10.html): 
- No progress for the day. Wasn't able to focus much. 
- So, spent most of the time in reading stuffs.

[Day 05](https://priyankasaggu11929.github.io/outreachy/2019/12/13/Outreachy-Day-11.html): 
- Finally succeeded in reverse engineering the *gnome-builder's* `search_and_replace_bar` widgets into its units. 
- This time, started picking up the concerned widget's source code (for recreation inside libdazzle's example application), the right way.

[Day 06](https://priyankasaggu11929.github.io/outreachy/2019/12/14/Outreachy-Day-12.html):
- Done recreating the widget into the example application. Still required to work more on the invoking action.
- Have started testing the re-created widget files in the *gtranslator* project as well.


