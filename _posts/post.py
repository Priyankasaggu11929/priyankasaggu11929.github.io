import os, os.path
from os import path
import tempfile, subprocess
from datetime import date, datetime, timedelta

yesterday=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

dir_path = os.path.dirname(os.path.realpath(__file__))

count =0
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.startswith(yesterday):
            file=str(file.strip(".md"))
            count = int(file[-1])

count+=1
today = date.today()

title = str(today)+"-Outreachy-Day-"+str(count)+".md"

print(title)

if not path.exists(title):
    file = open(title,"w")
    date = today.strftime("%B %d, %Y")
    data ="""---
layout: post
title: "Outreachy - Week __, Day __!"
description: "The Progress report of Day __ of work for Outreachy Program."
category: Outreachy
tags: [Outreachy, GNOME, GTranslator, Internship, Daily-Progress]
comments: false
---
"""+"\n"+ date + """

**Task for the week:**

- 

**Progress of the day:**

-

Till next time. o/

"""
    file.write(data)
    file.close()

subprocess.call(['vim', title])

