---
layout: post
title: "Outreachy - Week 01, Day 03!"
description: "The Progress report of Day 3 of work for Outreachy Program."
category: Outreachy
tags: [Outreachy, GNOME, GTranslator, Internship, Daily-Progress]
comments: false
---

December 05, 2019

**Task for the week:**

- Try to replicate the gnome-builder “search and replace bar” widget (just the wire-frame) in the Gtranslator project.

**Progress of the day:**

- Today was an extremely long day (even I am still working and it's 23:47 here). There is not much actual progress from the day though, but I definitely learnt a hell lot of new things. And there are even *more* left for me to *just* understand.

I am extremely tired now 😅, so compiling the rest of it in very short and quickly now. 
  
+ I'm yet to learn how to use `libdazzle` properly (and I literally spent my whole day figuring out just this only). None of my example projects worked as intended but definitely there is a considerable progress in terms that I can understand the required code much better way now.
   
+ Yesterday, Though I was able to build the `gnome-builder` project properly, I still was facing another major issue. Whenever I tried to run the project in Builder IDE, it was not reflecting any changes that I made in the source code. Rather it always ran the same as the installed Builder IDE instance. So, there was no way for me to understand the effects, the *changes in the source-code* were making to the application. Lastly, I had to reach out to my mentor only for the solution. And I am quoting his reply as-it-is here.

> Builder uses build profiles to build. 
>
> Check the build preferences in the builder.
> Click `top-left button -> Build preferences` and check the flatpak manifest that is being used.
>
> Maybe the problem is the installed application name. Because if the application name is `org.gnome.Builder`, and it is already running, then the build run for the *application under development*  won't launch a new instance.
>
> So, you can try to change the `app-id` property in the flatpak manifest file and use *org.gnome.BuilderDevel* or something like that instead.

  + Changing the `app-id` in the flatpak manifest file does work to a great extent for me. The build run is finally isolated from the actual installed application, but stil the changes are not being reflected. And that I am leaving for tomorrow now.

  + This whole process actually made  me learn how to write basic `meson.build` files from scratch and then the *flatpak manifest files* as well. Which ultimately makes it really easy for me to understand the basic project structure, build system, runtime, external dependencies used and a lot other things.

+ I was trying to build *[libdazzle/example/app](https://gitlab.gnome.org/GNOME/libdazzle/tree/master/examples/app)* as an individual project, but failed. I even took danigm's help but still I was not able to rectify the build files (which means I'm yet to learn a lot more when it comes to writing `meson.build` files for large projects). So, again leaving it for tommorow.

+ The best thing for the day was that I figured out another application that implements the `search` bar (not entirely but still something worth) as the `gnome-builder`'s. `Gedit` have a drop-down kind of `search-bar` that invokes with *ctrl-f* shortcut-keys. So, I can refer to the respective source-code for help.

+ I need to work a lot on my *focus* as today I spent half of the day just digging rabbit-holes for stuffs that were not needed at all. Hopefully, tomorrow will be better in terms of my *work-focus*.

+ Misc:
  + I spent a couple of hours rectifying `ERROR: Dependency "tepl-4" not found, tried pkgconfig and cmake`. I managed to get the package's git files but the master branch has some config errors. So, no solution so far.

That's all for today. 

(And the time is 00:59 now. Will straight-away jump to bed now.)

 Good night o/

### Resources:

1. Meson Tutorial (https://mesonbuild.com/Tutorial.html)
2. Flatpak Manifests (http://docs.flatpak.org/en/latest/manifests.html)
3. libdazzle example project (https://gitlab.gnome.org/GNOME/libdazzle/tree/master/examples/app)


