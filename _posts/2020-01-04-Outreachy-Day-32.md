---
layout: post
title: "Outreachy - Week 04 and 05!"
description: "The Progress report for Days 21 to 32 of work for Outreachy Program."
category: Outreachy
tags: [Outreachy, GNOME, GTranslator, Internship, Daily-Progress]
comments: false
---

January 04, 2020
[UPDATED]

**Task I'd for the last 2 weeks:**

- [X] <strike>Try to replicate the gnome-builder “search and replace bar” widget (just the wire-frame) in the Gtranslator project. [Half done]</strike> [Finally finished 🎉️]
  - [X] <strike>[sub-task] First try doing the above task in a seperate simple application.</strike> 

**Progress:**

- <strike>I finished the sub-task i.e replicating the gnome-builder's "search and replace bar" widget in the libdazzle example application (which basically is a really *big* step towards my final goal).</strike> I finished both the tasks, now it's definitely a big step. :)

![Libdazzle-example-application](/assets/example-search-bar.png)

- Yesterday (Januray 3, 2020), I had my first real-time problem-solving/debugging session with my mentor, [danigm](http://danigm.net). He spent a couple of hours, debugging some (long-standing) issues with my code and finally we had it running. It was really insightful looking at the way how he approached the problems, looked for solutions through the documentations on internet, utilized `GtkInspector` (the Gtk debugging tool) to it's best and meanwhile kept conveying what actually he was trying to do. It basically turned out to be more of a real-time *learning session*.

- <strike>Today, (with the help of yesterday's pointers) I re-created the same widget in gtranslator application. I think I'm almost done. There are some (maybe 1 or 2) broken signals to check and hopefully, I'll finish it very soon.</strike> DONE \o/

![Gtranslator-GtrTab-search-and-replace-bar](/assets/gtr-tab-search-bar.png)
![Gtranslator-recreated-search-and-replace-bar](/assets/gtranslator-search-bar.png)

- I opened the [first MR](https://gitlab.gnome.org/GNOME/gtranslator/merge_requests/56) for Outreachy (though a WIP). 

Although, I've compiled it very short but the work/learning/research I did in last 2 weeks was enormous. It's just that the process behind, was kind of really repetative and not discrete. So, I decided to update the final results only, for this time-being. 

Now, that I have achieved something tangible, I hope the coming days would be a little easier to proceed with.

That's all for now. o/
