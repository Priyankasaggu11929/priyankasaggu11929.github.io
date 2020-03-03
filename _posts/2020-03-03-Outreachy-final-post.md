---
layout: post
title: "Wrapping up Outreachy'19!"
description: "The post describing final thoughts about my Outreachy Internship!."
category: Outreachy
tags: [Outreachy, GNOME, GTranslator, Internship, Daily-Progress]
comments: false
---

March 03, 2020

Okay, the *final day of my outreachy internship*! :)

It's a mixed kind of feeling. I'm happy that I managed to finish what I aimed in the beginning, but a little sad too, as this (internship) run will end tommorrow. 

But there is this fact that ***Now, I am a part of GNOME Foundation***, makes me the most happiest. This is the sole reason why I applied to [Outreachy](https://www.outreachy.org/). I wanted to be a part of an open-source organisation, learn from the community there and then eventually contribute back. And here, I got my first some steps laid down (cherry on the cake, it's GNOME Foundation). :)

[Daniel García Moreno (danigm)](http://danigm.net/) and [Daniel Mustieles García (dmustieles)](https://versosparaundiacualquiera.blogspot.com/), I can't thank my mentors enough. Simply, It wouldn't have been possible without their incredible guidance. They're the best in their jobs (which here is a selfless volunteering & mentoring).

I would like to take a moment more to thank danigm for *all his time* that he spent solving my doubts, leading me to the right things whenever I reached him. Although I myself didn't manage to write consistently (even at one point, it was a total halt), I managed to read a lot about danigm in [his blogs](http://danigm.net) and everytime, it left me more inspired and much more motivated to do my work.

The [Planet GNOME](http://planet.gnome.org/) (the planet blogs feed for GNOME Foundation folks) was a constant source of information & knowledge.

Before I actually write about my final contribution here, I would like to leave a note about **what was my initial approach** that made me finally end up into GNOME Foundation. I basically had three things in my mind:

(*Although the approach was pretty straight forward, I think It might help the future outreachy applicats in some way*)

1. I remember I was looking for a project that invited applicants willing to learn and work together, during the span of the internship.
2. Second thing was the number of the intern positions (for me, I wanted to proceed in a project with less intern positions). 
3. And then the final and the most important thing was that I wished to learn either a whole new technology, or something that I would really appreciate having in my tech-stack. (It was C language that I was most afraid of, all this while, but I definitely wanted to learn and write some real code in it.)

![gtranslator-project-description-outreachy-dec-2019](/assets/gtranslator.png)

And the project [Gtranslator](https://wiki.gnome.org/Apps/Gtranslator) exactly gave me all these marks, in sequence. So, I was done with my project hunt and I immediately started contributing (to the best of mine) right from the very beginning (*october 1, 2019*) till the final results (*december 3, 2019* when the selected interns were announced). 

I swear, this initial contribution period gave me a *really* good insight about my project as whole. I felt really confident with my contributions once I got the real hang of it (once again, a huge thanks to my mentors. They're helpful *(being both responsive and guiding)* right from the beginning). 

Now, after a period of 13 weeks (3 months), I am here writing about my final contribution. :D

**Task** - Gtranslator: Rework the search and replace dialog.

**Approach**:

- We took inspiration from the existing search and replace dialog of the `gnome-builder` application and aimed to redesign our own widget, somewhat similar to what we have there. (Check this issue [here](https://gitlab.gnome.org/GNOME/gtranslator/issues/97) for more clarity)

- I started by learning how [libdazzle](https://github.com/GNOME/libdazzle) library works (as it is what `gnome-builder` project is using behind the required widget). So, the first few weeks, I worked on a dummy side project, in order to understand it's basic working. It took me a lot more time than what I estimated. But fortunately, I ended up being much more familier with the deep rabbit-hole concepts of my project. I've listed about what all things I learnt during the process, in sequence [here](https://priyankasaggu11929.github.io/outreachy.html).

- Once I finished doing the dummy project basics, I first re-created the wire-frame of the new search and replace dialog here itself. Then worked on solving the basic stuck issues (that I faced while this trial implementation) during the first screen-sharing session with danigm. 

- Then, I finally migrated the trial re-created widget source-code to `gtranslator` and started writing actual functionalities for the widget.

- By the time I finished having the actual wire-frame of the search and replace bar and it's basic hide/show functionality, right in place, 2 months of my internship were already over. Mark that I spent *alot* of days doing redundant tasks. (sadly that had put my daily writing on hold. Now, I wish I should've laid down that struggle as well. Because learning from re-doing stuffs is a *huge* gain as well.)

- The last month went onto migrating the actual search, find, and replace functionality from the existing old `search-and-replace-dialog` to the new overlay `search-and-replace-bar` widget.

**Final Outcome**:

<video width="800" height="350" controls>
  <source src="/assets/final-gtranslator.webm" type="video/mp4">
</video>

**Improvements required**:

- Correct callback for keyboard shortcut (Ctrl+h) for direct replace-mode invoke action.
- Add a message when no strings are found (or "end of file reached" when Wrap around is disabled).
- Detect when there are two or more occurrences of the expression (to be searched) in the same string.

As pointed by dmustieles,

> Example: "This is a dummy string with some dummy content in a dummy PO file"

> If you search "dummy" it will find and highlight the first match. Although the 2nd and the 3rd will also be found (pressing the arrow button in the widget doesn't moves to the follwing string) but occurrences are not highlighted.

- And some more I don't recall right now (have noted down 😅).

Although, this wraps up my Outreachy internship and the task under GNOME Foundation, I really don't want to stop it here. I aim and actually hope to be active in my own project and keep contributing to as much as I can.

Last week, I've started with a full-time job as a DevOps Engineer intern at [Atlan](http://atlan.com/). But honestly, I wish to work remotely sometime soon, in an open-source project and that too in DevOps/sys-admin domain. So, would love to explore more such opportunities from the GNOME Foundation itself and give them my best try.


Lastly, Before I wrap up this Outreachy journey, there are 2 more folks whom I want to give a *huge thanks* for their *enormous* guidance and *huge* support before and throughout this stretch. I wouldn't have reached here without their constant support and guidance.

Thank you, [(Kushal Das) kushal](http://kushaldas.in/)!

Thank you, [(Mario Jason Braganza) jasonbraganza](https://janusworx.com/)! :)

> I remember, kushal had once said, if I really want to repay him (for all his time, support and mentorship) in some way, it would be through the number of patches I'll submit to an open-source project. 

(I'm happy I've gathered a few submiited patches in my kitty now :) )


Signing off as an Outreachy Intern (December 3, 2019 - March 3, 2019)! o/
