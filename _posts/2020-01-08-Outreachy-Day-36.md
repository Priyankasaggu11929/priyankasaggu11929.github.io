---
layout: post
title: "Outreachy - Week 06, Day 03!"
description: "The Progress report of Day 36 of work for Outreachy Program."
category: Outreachy
tags: [Outreachy, GNOME, GTranslator, Internship, Daily-Progress]
comments: false
---

January 08, 2020

**Task for the week:**

- Move the existing search-and-replace-bar widget functionality to the new redesigned overlay widget.

**Progress of the day:**

- This week started on a good note. I spent the first 2 days working on the final nitpicks for the UI of the widget. 

- Today, I added CSS rules for creating a border around the "search entry and buttons grid". 

- Also, I corrected the position of the widget. Earlier it was rendering down below the event progress-bar and thus, the overlay effect was entirely absent. Therefore, I tweaked the corresponding xml file [src/gtr-tab.ui](https://gitlab.gnome.org/priyankasaggu119/gtranslator/blob/gtr-search-and-replace-bar/src/gtr-tab.ui#L10-206) to bind the two required child elements i.e one with `GtkPaned` class (on top of which the new widget will overlay) and the other with `GtkRevealer` class (which is supposed to overlay) together, and put them under `GtkOverlay` class. And it solved the issue.

![GtkInspector-elements](/assets/gtr-tab-ui.png)

With this, I have finally reached half way to finishing my project. :D 


<video width="800" height="350" controls>
  <source src="/assets/widget.webm" type="video/mp4">
</video>


Tomorrow onwards, I Will slowly start migrating existing functionalities to the newly designed widget.

That is all for now. :)

