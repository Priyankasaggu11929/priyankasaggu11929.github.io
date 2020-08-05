---
layout: post
title: "[Python for DevOps] Essentials for DevOps!"
description: "The notes for chapter 1 from the book, Python for DevOps."
category: Learning-Python
tags: [DevOps, Python, Notes]
comments: false
---

August 03, 2020

I've sort of started learning Python programming from scratch once again (I won't say I knew it well before as well, but it was more of an on-off thing that I learnt whenever required). So, I'm trying to bring my brain back to thinking in more real programming terms (here I mean writing actual code, not just the usual yaml, json or bash scripts that I keep writing all the time for automation during work).

Ok, now to the point!

I've started with the book **Python for DevOps** by *Noah Gift, Kennedy Behrman, Alfredo Deza, Grig Gheorghiu*. And the plan is to follow & finish it religiously as my first some steps.

---

### The Chapter 1, *Python Essentials for DevOps* touched the following topics briefly!

- [X] Installing and Running Python (Python Shell, IPython)
- [X] Procedural Programming (Variables, Basic Math, Comments, Built-in Functions, Print & Range)
- [X] Execution Control (if/elif/else, & for loops)
- [X] While Loops
- [X] Handling Exceptions
- [X] Built-in Objects
- [X] Functions
- [X] Using Regular Expressions
- [X] Lazy Evaluation 
       - [X] Generators
       - [X] Generator Comprehensions
- [X] More IPython Features
- [X] Exercises

---

- Till the *Handling Exceptions* and the first part of *Built in Objects*, I was quite familier with most of them. Although I was still not aware of the right terminologies, so I learnt & brushed up more of that during these sections.

---

> **Python variables use dynamic typing.** In practice, this means that they can be reassigned to values of different types or classes.
>
> For example:
> ```python
> big = 'large'
> big = 1000/1000
> big = {}
> ```
> Here the same variable is set to a string, a number, and a dictionary. Variables can be reassigned to values of any type.

---

- I have started using the docstrings finally. So, now hopefully my code will have some basic clean documentation.

---

> Though range is a built-in function, it is technically not a function at all. It is a type representing a sequence of numbers.
>
> When calling the range() constructor, an object representing a sequence of numbers is returned. Range objects count through a sequence of numbers.
>
>
> range maintains a small memory footprint, even over extended sequences, as it only stores the start, stop, and step values. The range function can iterate through long sequences of numbers without performance constraints.

---

-  And try & catch! I remember the first & last time I ever used `try-catch` blocks was during writing small sys-admin based problems in [kushal's](kushaldas.in) [lymworkbook](https://github.com/kushaldas/lymworkbook) project. Hopefully, I will write more now onwards!

- I'm not sure if it is right. But I've seen questions like *what's the difference between python functions & methods?*. To me, both were same, but just a slight difference stuck my attention, so I'm writing it here.
    - Python functions attached to objects and classes are referred to as `methods`.
    - So, (just assuming), any function outside a class, or not attached to objects are known as functions.
    - But broadly, the idea is still same for me!

---

> Sequences represent *ordered and finite collections of items*. 
>
> Sequences are a family of built-in types, including the list, tuple, range, string, and binary types.

---

- And now, the only thing I remember about lists from the time before starting with the book.

```python
# COPY A LIST

a = [1,2,3,4,5,6]

copy_of_a = a[:]

# REVERSE A LIST

reverse_of_a = a[::-1]
```

- In lists, there is also a `remove` method, which removes the first occurrence of an item.

```python
pies = ['cherry', 'cream', 'apple', 'rhubarb']

# pop () will pop/remove & return the last item from the list pies.

pies.pop()

# remove() will remove the first occurrence of an item in the list.

pies.remove('apple')
```

- As of Python 3, strings default to using **UTF-8 encoding**.

---

> The split method breaks a string into a list of strings. By default, it uses whitespace as the token to make the breaks. An optional argument can be used to add in another character where the split can break.
>
> ```python
> text = "Mary had a little lamb"
>
> # SPLIT THE STRING BY WHITESPACE AS DELIMITER
>
> items = text.split()
> ['Mary', 'had', 'a', 'little', 'lamb']
>
> # NOW JOINING THE SPLITTED STRING WITH "-" AS CONNECTOR!
>
> "-".join(items)
> `Mary-had-a-little-lamb`
> ```

---

> You can also specify format specification arguments. Here they add left and right padding using > and <. In the second example, we specify a character to use in the padding:
>
> ```python
> text = "|{0:>22}||{0:<22}|"
> text.format('O','O')
> 
> # OUTPUT
> '|                     O||O                     |'
>
> text = "|{0:<>22}||{0:><22}|"
> text.format('O','O')
>
> # OUTPUT
> '|<<<<<<<<<<<<<<<<<<<<<O||O>>>>>>>>>>>>>>>>>>>>>|'
> ```

- Format specifications are done using the [format specification mini-language](https://docs.python.org/3/library/string.html#format-specification-mini-language). 

---

> A mutable object is one whose contents can change in place. Lists are a primary example; the contents of the list can change without the list’s identity changing. Strings are not mutable. You create a new string each time you change the contents of an existing one.

---

- If the key is not in the dict, it adds as a new entry. If it already exists, the value changes to the new value:

```python
map = {'key-1': 'value-1', 'key-2': 'value-2'}
>>> map['key-3'] = 'value-3'
>>> map
{'key-1': 'value-1', 'key-2': 'value-2', 'key-3': 'value-3'}
>>> map['key-1'] = 13
>>> map
{'key-1': 13, 'key-2': 'value-2', 'key-3': 'value-3'}
```

- You can check to see if the key exists in a dict using the syntax below. In the case of dicts, **it checks for the existence of keys**:

```python
>>> if 'key-4' in map:
...     print(map['key-4'])
... else:
...     print('key-4 not there')
...
...
key-4 not there
```

- Just writing a note for myself that `get()` & `del()` functions for Python dictionary have different syntax.

```python
# Different syntax

b = {1:2, 3:4, 5:6}

b.get(1)

del(b[5])
```
---

- There are three types of comprehensions I learnt so far,
    1. List Comprehensions: [x%x for x in range(10)]
    2. Dict Comprehensions: {x:x%x for x in range(10)}
    3. Generator Comprehensions: (x%x for x in range(10))

---

- **Functions are objects.** They can be passed around, or stored in data structures. You can define two functions, put them in a list, and then iterate through the list to invoke them:

```python
>>> def double(input):
...     '''double input'''
...     return input*2
...
>>> double
<function double at 0x107d34ae8>
>>> type(double)
<class 'function'>
>>> def triple(input):
...     '''Triple input'''
...     return input*3
...
>>> functions = [double, triple]
>>> for function in functions:
...     print(function(3))
...
...
6
9
```

- **Anonymous Functions**: When you need to create a very limited function, you can create an unnamed (anonymous) one using the `lambda` keyword. 
    -  Generally, you should limit their use to situations where a function expects a small function as a argument.

> In this example, you take a list of lists and sort it. The default sorting mechanism compares based on the first item of each sublist:
>
> ```python
> items = [[0, 'a', 2], [5, 'b', 0], [2, 'c', 1]]
> sorted(items)
> 
> # OUTPUT
> [[0, 'a', 2], [2, 'c', 1], [5, 'b', 0]]
> ```
> To sort based on something other than the first entry, you can define a method which returns the item’s second entry and pass it into the sorting function’s key parameter:
>
> ```python
> def second(item):
>      '''return second entry'''
>       return item[1]
>
> sorted(items, key=second)
>
> # OUTPUT
> [[0, 'a', 2], [5, 'b', 0], [2, 'c', 1]]
> ```
> With the `lambda` keyword, you can do the same thing without the full function definition. Lambdas work with the lambda keyword followed by a parameter name, a colon, and a return value:
>
> `lambda <PARAM>: <RETURN EXPRESSION>`
>
> Sort using lambdas, first using the second entry and then using the third:
>
> ```python
> sorted(items, key=lambda item: item[1])
>
> # OUTPUT
> [[0, 'a', 2], [5, 'b', 0], [2, 'c', 1]] 
>
> sorted(items, key=lambda item: item[2])
>
> # OUTPUT
> [[5, 'b', 0], [2, 'c', 1], [0, 'a', 2]]
> ```

---

- [Regular Expressions] You can use the `re.search` function, which returns `a re.Match` object only if there is a match:

```python
In [3]: import re

In [4]: re.search(r'Rostam', cc_list)
Out[4]: <re.Match object; span=(32, 38), match='Rostam'>
```

- You can use parentheses to define groups in a match. These groups can be accessed from the match object. They are numbered in the order they appear, with the zero group being the full match.

```python
>>> re.search(r'(\w+)\@(\w+)\.(\w+)', cc_list)
<re.Match object; span=(13, 29), match='ekoenig@vpwk.com'>
>>> matched = re.search(r'(\w+)\@(\w+)\.(\w+)', cc_list)
>>> matched.group(0)
'ekoenig@vpwk.com'
>>> matched.group(1)
'ekoenig'
>>> matched.group(2)
'vpwk'
>>> matched.group(3)
'com'
```

- And you can also supply names for the groups by adding `?P<NAME>` in the group definition. Then you can access the groups by name instead of number.

```python
>>> matched = re.search(r'(?P<name>\w+)\@(?P<SLD>\w+)\.(?P<TLD>\w+)', cc_list)
>>> matched.group('name')
'ekoenig'
```

- `re.search()` returns just the first maych found. We can also use `re.findall()` to return all of the matches as a list of strings.

```python
>>> matched = re.findall(r'\w+\@\w+\.\w+', cc_list)
>>> matched
['ekoenig@vpwk.com', 'rostam@vpwk.com', 'ctomson@vpwk.com', 'cbaio@vpwk.com']
```

- When dealing with large texts, such as logs, it is useful to not process the text all at once. You can produce an iterator object using the `re.finditer()` method. 
    - This object processes text until it finds a match and then stops. 
    - Passing it to the `next()` function returns the current match and continues processing until finding the next match. 
    - In this way, you can deal with each match individually without devoting resources to process all of the input at once.

```python
>>> matched = re.finditer(r'\w+\@\w+\.\w+', cc_list)
>>> matched
<callable_iterator object at 0x108e68748>
>>> next(matched)
<re.Match object; span=(13, 29), match='ekoenig@vpwk.com'>
>>> next(matched)
<re.Match object; span=(51, 66), match='rostam@vpwk.com'>
>>> next(matched)
<re.Match object; span=(83, 99), match='ctomson@vpwk.com'>
```

- [regex for subsitution] Besides searching and matching, regexes can be used to substitute part or all of a string.

```python
>>> re.sub("\d", "#", "The passcode you entered was  09876")
'The passcode you entered was  #####'
```

- [regex compiling] All of the examples so far have called methods on the re module directly. This is adequate for many cases, but if the same match is going to happen many times, performance gains can be had by compiling the regular expression into an object. This object can be reused for matches without recompiling:

```python
>>> regex = re.compile(r'\w+\@\w+\.\w+')
>>> regex.search(cc_list)
<re.Match object; span=(13, 29), match='ekoenig@vpwk.com'>
```

---

- [Generators - Lazy Evaluation]
    - To write a generator function, use the yield keyword rather than a return statement.
    - Every time the generator is called, it returns the value specified by `yield` and then pauses its state until it is next called.
    - Example: a generator that simply counts, returning each subsequent number.

```python
>>> def count():
...     n = 0
...     while True:
...         n += 1
...         yield n
...
...
>>> counter = count()
>>> counter
<generator object count at 0x10e8509a8>
>>> next(counter)
1
>>> next(counter)
2
>>> next(counter)
3
```

---

- We can see the difference in memory used by using the `sys.getsizeof` method, which returns the size of an object, in bytes:

```python
>>> import sys
>>> list_o_nums = [x for x in range(100)]
>>> gen_o_nums = (x for x in range(100))
>>>
>>> sys.getsizeof(list_o_nums)
912
>>> sys.getsizeof(gen_o_nums)
120
```

- And finally, I've a Python IDE/Editor (other than my all time solution, vanilla vim). I'm loving IPython! :)

---

### From the Chapter 2, *Automating Files and the Filesystem*  I've covered a little so far...

- [X] Reading and Writing Files

---

- You can use the `open()` function to create a file object that can read and write files. 
    - It takes two arguments, the `path of the file` and the `mode` (mode optionally defaults to reading). 
    - You use the mode to indicate, among other things, if you want to read or write a file and if it is text or binary data.  

```python
with open(file_path, 'r') as open_file:
    text = open_file.readlines()

open_file.closed

# OUTPUT
True
```

- While using `with` keyword to open files like in the above example, Python implicitely closes the file (and so `open_file.closed` returned True). Other times, we need to explicitely close the file like `open_file.close()`.

- Different operating systems use different escaped characters to represent line endings. Unix systems use `\n` and Windows systems use `\r\n`. Python converts these to `\n` when you open a file as text.

- And then I read about `json` module to nicely parse json files in a structured manner.

```python
import json

with open(`service-policy.json`, `r`) as opened_file:
	policy = json.load(opened_file)
```

- `json.dump()`  in case of file opened in write mode, will update the changes in the file.

- I learnt about `pprint` module which is used for pretty printing. It automatically formats Python objects for printing. Its output is often more easily read and is a handy way of looking at nested data structures.

- Then I read about `PyYAML` module which is not included in the Python Standard Library, but you can install it using pip, `pip install PyYAML`.

- And stupid me, I was trying to import the module as `import PyYAML` (didn't even cared to read 2 more lines from the book) for some 15-20 minutes & marked my python setup had some issue. :|

```python
import yaml

with open('verify-apache.yml', 'r') as opened_file:
     verify_apache = yaml.safe_load(opened_file)

pprint(verify_apache)
```	 
- Similarly, `yaml.dump()` wll save Python data to a file in YAML format.

- And then I read about dealing with XML files. So, got to know about `xml.etree.ElementTree` module, then `requests` & `xmltodict` module (last one, I needed to install using pip).

```python
import requests 
import xmltodict 

url = "https://janusworx.com/rss.xml" 
response = requests.get(url) 
data = xmltodict.parse(response.content) 
```

- And then finally, `csv` module for dealing with CSV (comma separated values) files.
    - The csv reader object iterates through the .csv file one line at a time, allowing you to process the data one row at a time. 

```python
import csv
with open(file_path, newline='') as csv_file:
	off_reader = csv.reader(csv_file, delimiter=',')
        for _ in range(5):
           print(next(off_reader))
```
