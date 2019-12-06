---
layout: post
title: "Outreachy - Week 01, Day 04!"
description: "The Progress report of Day 4 of work for Outreachy Program."
category: Outreachy
tags: [Outreachy, GNOME, GTranslator, Internship, Daily-Progress]
comments: false
---

December 06, 2019

**Task for the week:**

- <strike>Try to replicate the gnome-builder “search and replace bar” widget (just the wire-frame) in the Gtranslator project.</strike> (Hopefully, I will continue it sometime in the next week)
- Understand the structure and working of [libdazzle's example application](https://gitlab.gnome.org/GNOME/libdazzle/blob/master/examples/app).

**Progress of the day:**

Today was good. Fortunately, I wasted (almost) no time in solving application build errors. Besides, I even started writing actual code which didn't work properly though, but I'm happy that atleast I managed to start from somewhere. :)

+ I started the day continuing building the `Gedit` application. It was smooth but there was a lot to do before I actually got it working. Meson marked almost half of the runtime dependencies as missing. So, I'd to install them manually. I'm writing my process here, hoping it might help someone else facing the same issues later.
  - The first one was `Tepl`. If you get this error, I seriously recommend not to check the gitlab/github repository at all (you'll end up wasting all your time and still it won't work). The best solution is to look for the source tarball on GNOME wiki [here](https://wiki.gnome.org/Projects/Tepl). I needed to install `amtk-5` & `uchardet` as well before. The steps to install are simple ( the same will go for almost all the other dependencies as well):
```
$ ./configure
$ make
# change into root if required.
$ make install
```
  - Now, the process will be same for rest of the missing dependencies as well. So, just naming them here. You can find the respective tarballs on their GNOME wiki project pages.
     1. libpeas
     2. libsoup
     3. libsoup
     4. gspell
     5. enchant

  - After installing all these missing dependencies, the next error was `Couldn't find include 'GtkSource-4.gir' (search path: '['/usr/share/gir-1.0', '/usr/share', 'gir-1.0', '/usr/share/gir-1.0', '/usr/share/gir-1.0']')`. The *GtkSource-4.gir* file was actually present in the path */usr/local/share/gir-1.0/*. Thus, creating a symlink of the file to the required search path i.e. */usr/share/gir-1.0* solved the issue.

  - Lastly, the `ittools` module was missing. So, simply installing it from the debian package manager, finally ended into the successful run o Gedit build. :)

+ After getting the Gedit build running, next step was to understand it's `search bar` implemenation by making modifications in the source-code. It was defintely worth spending time on but soon I realised I should better focus on the *libdazzle implementation* (in *gnome-builder* application) only. As the latter is more code-efficient and exactly the way I am *actually* supposed to do. Gedit's implementation of just *search-bar*itself is around 1500 lines of code, where gnome-builder using *libdazzle* implements the whole search-and-replace combo in just 1/3rd of the total.

+ Next then, I started copying source code for `search-and-replace-bar` from gnome-builder's `src/libide/editor/ide-editor-search-bar.c` file and it's respective headers into *gtranslator* (good gracious, finally I'm back to my own project). And as expected it didn't work. Even though, it's just 1/3rd of the Gedit's implementation but still around 600 lines of code, and simply copying will surely not work. Therefore, the only solution left is to take some step backwards and learn how to use *libdazzle* from scratch via it's example application tutorial. (And that is why the task for the week is changed now.)

+ Learning from the last time's failure of trying building the *[example/app](https://gitlab.gnome.org/GNOME/libdazzle/blob/master/examples/app)* project as a separate individual project, this time I've taken one more step back. I will first cover up the flaptpak's *[Getting started](http://docs.flatpak.org/en/latest/first-build.html)* documentation and then will try building it again from start. Hopefully, it'll turn out to be a good foundation. Or if nothing works, then at last, will discuss it again with danigm in the first weekly meeting.

+ I also learnt writing proper `struct`s. (I know it is quite simple for most others, but I never wrote them earlier, thus, needed some good insights.)

(I am quite satisfied with my today's progress. Atleast, I have some takeaways to decide my further plannings. )

That's all for now. 

Till tomorrow. o/

