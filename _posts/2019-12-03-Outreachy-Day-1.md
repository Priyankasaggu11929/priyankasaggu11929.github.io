---
layout: post
title: "Outreachy - Day 1!"
description: "The Progress report of Day 1 of work for Outreachy Program."
category: Outreachy
tags: [Outreachy, GNOME, GTranslator, Internship, Daily-Progress]
comments: false
---

December 3, 2019

Okay, **finally** the Outreachy Internship has started! 🎉 🎉

For this very moment, nothing could make me happier for the fact that I earned this chance to pursue it under a very highly reputed Open Source project, the [GNOME Foundation](https://www.gnome.org/foundation/) 🙂. 

Soon, I will try to write a more detailed post thanking all the awesome people who have endlessly helped me being capable of reaching out to this milestone (and hopefully to some more as I continue to progress). At the same time, I'll lay down my experience so far, so that the upcoming Outreachy aspirants could take away some key-points to ease their process of applying.

Now, before I proceed, I'd like to take this moment to profusely thank my *Project Mentors*, [Daniel García Moreno (danigm)](http://danigm.net) and [Daniel Mustieles García (dmustieles)](https://versosparaundiacualquiera.blogspot.com/) for being incredibly generous with their time and energy and always being a source of immense encouragement and guidance to me.

And with that, finally, it's time for the *use-case* of this blog post i.e. **Progress for the Outreachy Day-1**.

- Today was a very long day (I spent approx. more than 10 hours majorly fixing my local GNOME build environment which is still not done. After an exhaustive try for the whole day, now I have left it for tomorrow.)
- Though I am familiar with the [Project](https://gitlab.gnome.org/GNOME/gtranslator) for about more than a month and a half now, I was still not (satisfactorily) versed with various components of the GNOME build environment. I had no idea that there are multiple [runtimes](http://docs.flatpak.org/en/latest/available-runtimes.html) and build systems/tools available such as JhBuild, etc. And even didn't know much about what [flatpak](https://flatpak.org/) and [flathub](https://flathub.org/home) are & needed for (that is not a good thing at my part, but that is what how it was and I am not proud). But because I had to build the environment back again today all from start, I read extensively about these so far ** unknown things** (which I am proud of now :P ).
- For this first week, I am supposed to check ( & understand) and build the `[gnome-builder](https://wiki.gnome.org/Apps/Builder)` project and try to re-create it's respective `search and replace dialog` in my project. About today, for the maximum time, I was stuck at trying getting rid of this runtime dependency error `meson.build:260:0: ERROR: Dependency "gtksourceview-4" not found, tried pkgconfig and cmake` (and stuck even now and that is why the re-building of the environment is for). Though I applied some pointers given by danigm but failed miserably, so now tomorrow, I will check again what I am doing wrong or what could be the alternative solutions to it.
- I realized I have to be super-observant of the flatpak versions and thus, the updates in case of build failures. Because, as danigm pointed out the `gnome-builder` build fail was since the 'gtksourceview' dependency has already moved inside the SDK itself. So, it doesn't require to add this dependency anymore (https://mail.gnome.org/archives/desktop-devel-list/2019-December/msg00001.html).

I guess that is all for my Day 1. I am calling it off now!

Till next time, o/
