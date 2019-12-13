---
layout: post
title: "Outreachy - Week 02, Day 05!"
description: "The Progress report of Day 11 of work for Outreachy Program."
category: Outreachy
tags: [Outreachy, GNOME, GTranslator, Internship, Daily-Progress]
comments: false
---

December 13, 2019

**Task for the week:**

- Try to replicate the gnome-builder “search and replace bar” widget (just the wire-frame) in the Gtranslator project.
   - [sub-task] First try doing the above task in a seperate simple application. 

**Progress of the day:**

- Today was a highly productive day. 

- For all these days, I was trying to re-create the `search_and_replace_bar` widget from `gnome-builder` but it was not happening only. The reason being I was not able to understand how exactly the widget was written (I knew what were the concerned files but still where to start in those files, in order to re-create it, I honestly had no idea). My approach was to reverse-engineer the `gnome-builder`'s widget and see how various stuffs are linked together and what things are invoking actions. 

(*Finally finally finally, it happened today.*)

-  I was able to break the widget into it's units (I'm sooo proud of myself XD). It was hard to figure out (for me atleast, because I have just started writing scratch code), but now I have it. \o/

- So, once I knew how it was written, It was a bit easier (not *really* easy but comparatively, yes) to start picking up the code to re-create it into another application. I spent half of the day copying the widget to my simple *libdazzle-example* application. I'm definitely having a *really* good progress now. I have picked up around some 5000-6000 lines of code so far and I think It'll require some more to run properly. (when I say "picking up", it's not *exactly* copy-pasting. I had to modify more than half of the lines of codes. And then even had to figure out what will go where in order to put the pieces back in shape (and running). ) 

- I hope in the coming days, I'll achieve some tangible results to showcase here.

That's all for today.

Till tomorrow. o/

Good night! 

