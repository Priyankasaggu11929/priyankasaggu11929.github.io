---
layout: post
title: "Site Reliability Engineering - Chapter 1!"
description: "The takeaways from chapter 1 of the Google's SRE book!"
category: SRE
tags: [SRE]
comments: false
---

July 19, 2020

The [Google's Site Reliability Enginnering](https://landing.google.com/sre/sre-book/toc/index.html) is the one of the books, that have been recommended or talked about by almost all the experienced DevOps, SRE, or cloud/infrastructure engineers, I ever got a chance to have a conversation.

Even in some of my recent interviews, there were discussions around the book. So, I no longer need any more facts to convice myself that this book *is* certainly a must read not only for the DevOps/SRE/Cloud/Infra engineers, but (because now that I've read some part of it) for the core IT & software engineers too.

Today, I finished the first chapter from the book, which is an introduction to the SRE, the various approach to service management outside (the traditional Sysadmin approach) & inside Google, and finally a brief yet detailed discussion around tenants of SRE.

It's absolutely a gem of information. Even the *Preface* of the book itself gave me my first set of learnings!

In this post here, I'll be quoting just a few of the things that inspired me the most, or some other facts that I learnt, or found quite interesting!

---

I got super duper inspired when I got to read about *Margaret Hamilton*. She (*according to the book*) is the first ever *Site Reliability Engineer*.

What could be more exciting than learning about a woman as the first SRE. But sadly, just like other woman pioneers, *Margaret* also had to face rejections & ignorance around her work.

>And taking the historical view, who, then, looking back, might be the first SRE?
>
>We like to think that Margaret Hamilton, working on the Apollo program on loan from MIT, had all of the significant traits of the first SRE.5 In her own words, "part of the culture was to learn from everyone and everything, including from that which one would least expect."
>
>A case in point was when her young daughter Lauren came to work with her one day, while some of the team were running mission scenarios on the hybrid simulation computer. As young children do, Lauren went exploring, and she caused a "mission" to crash by selecting the DSKY keys in an unexpected way, alerting the team as to what would happen if the prelaunch program, P01, were inadvertently selected by a real astronaut during a real mission, during real midcourse. (Launching P01 inadvertently on a real mission would be a major problem, because it wipes out navigation data, and the computer was not equipped to pilot the craft with no navigation data.)
>
>With an SRE’s instincts, Margaret submitted a program change request to add special error checking code in the on­board flight software in case an astronaut should, by accident, happen to select P01 during flight. But this move was considered unnecessary by the "higher-ups" at NASA: of course, that could never happen! So instead of adding error checking code, Margaret updated the mission specifications documentation to say the equivalent of "Do not select P01 during flight." (Apparently the update was amusing to many on the project, who had been told many times that astronauts would not make any mistakes—after all, they were trained to be perfect.)
>
>Well, Margaret’s suggested safeguard was only considered unnecessary until the very next mission, on Apollo 8, just days after the specifications update. During midcourse on the fourth day of flight with the astronauts Jim Lovell, William Anders, and Frank Borman on board, Jim Lovell selected P01 by mistake—as it happens, on Christmas Day—creating much havoc for all involved. This was a critical problem, because in the absence of a workaround, no navigation data meant the astronauts were never coming home. Thankfully, the documentation update had explicitly called this possibility out, and was invaluable in figuring out how to upload usable data and recover the mission, with not much time to spare.
>
>As Margaret says, "a thorough understanding of how to operate the systems was not enough to prevent human errors," and the change request to add error detection and recovery software to the prelaunch program P01 was approved shortly afterwards.

---

**Ben Treynor Sloss**, the senior VP overseeing technical operations at Google is the originator of the term "Site Reliability Engineering".

---

>Google’s rule of thumb is that an SRE team must spend the 50% of its time actually doing development. So how do we enforce that threshold? In the first place, we have to measure how SRE time is spent. With that measurement in hand, we ensure that the teams consistently spending less than 50% of their time on development work change their practices. Often this means shifting some of the operations burden back to the development team, or adding staff to the team without assigning that team additional operational responsibilities. Consciously maintaining this balance between ops and development work allows us to ensure that SREs have the bandwidth to engage in creative, autonomous engineering, while still retaining the wisdom gleaned from the operations side of running a service.

---

I want to quote this whole section around **Monitoring** here. It reminds me of the one question that I was asked in one of my very recent interviews. I feel like the book answers it in just the right words!

>Monitoring is one of the primary means by which service owners keep track of a system’s health and availability. As such, monitoring strategy should be constructed thoughtfully. A classic and common approach to monitoring is to watch for a specific value or condition, and then to trigger an email alert when that value is exceeded or that condition occurs. However, this type of email alerting is not an effective solution: a system that requires a human to read an email and decide whether or not some type of action needs to be taken in response is fundamentally flawed. Monitoring should never require a human to interpret any part of the alerting domain. Instead, software should do the interpreting, and humans should be notified only when they need to take action.
>
>There are three kinds of valid monitoring output:
>
> 1. Alerts
Signify that a human needs to take action immediately in response to something that is either happening or about to happen, in order to improve the situation.
>
> 2. Tickets
>Signify that a human needs to take action, but not immediately. The system cannot automatically handle the situation, but if a human takes action in a few days, no damage will result.
>
> 3. Logging
>No one needs to look at this information, but it is recorded for diagnostic or forensic purposes. The expectation is that no one reads logs unless something else prompts them to do so.

---

**Emergency Response**

>Humans add latency. Even if a given system experiences more actual failures, a system that can avoid emergencies that require human intervention will have higher availability than a system that requires hands-on intervention. When humans are necessary, we have found that thinking through and recording the best practices ahead of time in a "playbook" produces roughly a 3x improvement in MTTR (mean time to repair) as compared to the strategy of "winging it." The hero jack-of-all-trades on-call engineer does work, but the practiced on-call engineer armed with a playbook works much better. While no playbook, no matter how comprehensive it may be, is a substitute for smart engineers able to think on the fly, clear and thorough troubleshooting steps and tips are valuable when responding to a high-stakes or time-sensitive page. Thus, Google SRE relies on on-call playbooks, in addition to exercises such as the "Wheel of Misfortune,"7 to prepare engineers to react to on-call events.

---


