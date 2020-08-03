import os, os.path
from os import path
import tempfile, subprocess
from datetime import date, datetime, timedelta

yesterday=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

dir_path = os.path.dirname(os.path.realpath(__file__))

count =0
for root, dirs, files in os.walk(dir_path):
    for fi in files:
        if fi.startswith(yesterday) and fi.endswith(".md"):
            fi = str(fi.strip(".md"))
            print(fi)
            count = int(fi[-1])

count+=1
today = date.today()

inp=input("Enter the title: ")

title = str(today)+"-"+inp+".md"

print(title)

if not path.exists(title):
    fi = open(title,"w")
    date = today.strftime("%B %d, %Y")
    data ="""---
layout: post
title: ""
description: ""
category: something
tags: [something]
comments: false
---

"""+"\n"+ date + """

"""

    fi.write(data)
    fi.close()

subprocess.call(['vim', title])

