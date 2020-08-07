---
layout: post
title: "[Python for DevOps] Working with the Command Line - Part 1!"
description: "This post contain notes from Chapter-3 'Working with the Command Line' from the book, Python for DevOps!"
category: learning-python
tags: [DevOps, Python, Notes]
comments: false
---

August 07, 2020

So far, my journey around learning Python is on a nice track. And I'm trying my best to keep it up & going!

So, moving forward in the book, *"Python for DevOps"*, yesterday I finished the third chapter, *Working with the command line*! And I must say, now it's no longer me learning python once again (that was till some parts of the first chapter). Now, it's simply, *me learning python!* (all from kind of scratch & for the first time!)

So, from the third chapter, I covered the following topics:

- [X] Working with the Shell
    - [X] Talking to the Interpreter with the sys Module
    - [X] Dealing with the Operating System Using the os Module
    - [X] Spawn Processes with the subprocess Module
- [X] Creating Command-Line Tools
    - [X] Using sys.argv
    - [X] Using argparse
    - [X] Using click
    - [X] fire
    - [X] Implementing Plug-ins
- [X] Exercises

What I skipped (after taking a read only) is:

- Case Study: Turbocharging Python with Command-Line Tools
   - Using the Numba Just-in-Time (JIT) Compiler
   - Using the GPU with CUDA Python
   - Running True Multicore Multithreaded Python Using Numba
   - KMeans Clustering

And apart from the above, I also got to know about:

- Python function decorators
- Python classes

---

This chapter broadly introduced me to interacting with systems & shells using python. Further expanding to writing *command line tools* with Python, from (almost) scratch to building them using feature-loaded python modules.

- It's essential to be familiar with the `sys`, `os`, and `subprocess` modules, for interacting with systems and shells.

>There are two dominant ways to interpret bytes during reading. The first, *little endian*, interprets each subsequent byte as having higher significance (representing a larger digit). The other, *big endian*, assumes the first byte has the greatest significance and moves down from there.

More about *big endian & little endian* [here](https://chortle.ccsu.edu/AssemblyTutorial/Chapter-15/ass15_3.html).

- You could check the byte order of your current architecture as:

```python
In [1]: import sys

In [2]: sys.byteorder
Out[2]: 'little'
```		

- You can use `sys.getsizeof` to see the size of Python objects. **This is useful if you are dealing with limited memory**.

```python
In [3]: sys.getsizeof(1)
Out[3]: 28
```

- `sys.platform` gives the name of the current system platform.

- For knowing about the version of Python on your currently running python interpreter, use the attribute `sys.version_info`.

```python
n [4]: sys.version_info                                                                     
Out[4]: sys.version_info(major=3, minor=8, micro=2, releaselevel='final', serial=0)
```

- So, you can access the individual informations using attributes like, `sys.version_info.major`, `sys.version_info.minor`, `sys.version_info.micro`, `sys.version_info.releaselevels` & `sys.version_info.serial`.

---

- Following are examples from `os` module.

```python
In [1]: import os

# Get the current working directory.
In [2]: os.getcwd() 
Out[2]: '/home/priyankasaggu119/Desktop/.myhome/python-study'

# Change the current working directory
In [3]: os.chdir('/tmp') 

In [4]: os.getcwd()
Out[4]: '/private/tmp'

# The os.environ holds the environment variables that were set when the os module was loaded.
In [5]: os.environ.get('LOGLEVEL') 

# This is the setting and environment variable. This setting exists for subprocesses spawned from this code.
In [6]: os.environ['LOGLEVEL'] = 'DEBUG' 4

In [7]: os.environ.get('LOGLEVEL')
Out[7]: 'DEBUG'

# This is the login of the user in the terminal that spawned this process.
In [8]: os.getlogin()
Out[8]: 'priyankasaggu119'
```

- The most common usage of the os module is to get settings from environment variables. These could be the level to set your logging, or secrets such as API keys.

---

> There are many instances when you need to run applications outside of Python from within your Python code. This could be built-in shell commands, Bash scripts, or any other command-line application. To do this, you spawn a new process (instance of the application). 
>
> The `subprocess` module is the right choice when you want to spawn a process and run commands within it. With `subprocess`, you can run your favorite shell command or other command-line software and collect its output from within Python. For the majority of use cases, you should use the `subprocess.run` function to spawn processes.

```python
In [1]: import subprocess                                                                      
In [2]: cp = subprocess.run(['date', '--utc'], capture_output=True, universal_newlines=True, ch
   ...: eck=True )                                                                             

In [3]: cp.stdout                                                                              
Out[3]: 'Friday 07 August 2020 03:10:06 AM UTC\n'

In [4]: cp.stderr                                                                              
Out[4]: ''
```

(*Here, for the first time I got to know about the `--utc` flag for checking date & time in UTC. All the while, the browser was the option! :')*)

---

- When you construct a Python script, any statements at the top level (not nested in code blocks) run whenever the script is invoked or imported. So, for example, in both the following cases, the function `say_it` will be invoked at the top level.

```python
def say_it():
    greeting = 'Hello'
    target = 'Joe'
    message = f'{greeting} {target}'
    print(message)

say_it()
```
- When the script runs on the command line.

```bash
$ python always_say_it.py

Hello Joe
```
- Also, when the file is imported.

```python
In [1]: import always_say_it
Hello Joe
```
- Someone who is importing your module usually wants control over when its contents are invoked. You can add functionality that only happens when called from the command line by using the global `name` variable (i.e __name__).

- This `name` variable reports the name of the module during import. If the module is called directly on the command line, this sets it to the string `main`. So, we check for whether `__name__` is equal to `__main__`, and thus the updated script will be:

```python
def say_it():
    greeting = 'Hello'
    target = 'Joe'
    message = f'{greeting} {target}'
    print(message)

if __name__ == '__main__':
    say_it()
```

---

- To eliminate the need to explicitly call type python on the command line when you run your script, you can add the shabang `#!/usr/bin/env python` to the top of your file.

---

> The first step in creating command-line tools is separating code that should only run when invoked on the command line. The next step is to accept command-line arguments. Unless your tool only does one thing, you need to accept commands to know what to do. Also, command-line tools that do more than the simplest tasks accept optional flags to configure their workings. Remember that these commands and flags are the user interface (UI) for anyone using your tools. You need to consider how easy they are to use and understand. Providing documentation is an essential part of making your code understandable.

- The simplest and most basic way to process arguments from the command line is to use the `argv` attribute of the `sys` module. 
    - This attribute is a list of arguments passed to a Python script at runtime.
    - If the script runs on the command line, the first argument is the name of the script. The rest of the items in the list are any remaining command-line arguments, represented as strings.

```python3
In [1]: %%writefile sys_argv.py 
   ...:  #!/usr/bin/env python 
   ...: """ 
   ...: Simple command-line tool using sys.argv 
   ...: """ 
   ...: import sys 
   ...:  
   ...: if __name__ == '__main__': 
   ...:     print(f"The first argument:  '{sys.argv[0]}'") 
   ...:     print(f"The second argument: '{sys.argv[1]}'") 
   ...:     print(f"The third argument:  '{sys.argv[2]}'") 
   ...:     print(f"The fourth argument: '{sys.argv[3]}'") 
Writing sys_argv.py

In [2]: !python3 sys_argv.py arg1 arg2 arg3                                                    
The first argument:  'sys_argv.py'
The second argument: 'arg1'
The third argument:  'arg2'
The fourth argument: 'arg3'
```

- Here an example, where we're re-implementing the above `say_it()` function using `sys.arg` (basically implementing it as a argument parser).

```python3
In [7]: %%writefile sys_argv.py 
   ...: #!/usr/bin/env python 
   ...: """ 
   ...: Simple command-line tool using sys.argv 
   ...: """ 
   ...: import sys 
   ...:  
   ...: def say_it(greeting, target): 
   ...:     message = f'{greeting} {target}' 
   ...:     print(message) 
   ...:  
   ...: # Here we test to see if we are running from the command line. 
   ...: if __name__ == '__main__': 
   ...:  
   ...:     # Default values are set in these two lines. 
   ...:     greeting = 'Hello' 
   ...:     target = 'Joe' 
   ...:  
   ...:     # Check if the string --help is in the list of arguments. 
   ...:     if '--help' in sys.argv: 
   ...:         help_message = f"Usage: {sys.argv[0]} --name <NAME> --greeting <GREETING>" 
   ...:         print(help_message) 
   ...:  
   ...:         # Exit the program after printing the help message. 
   ...:         sys.exit() 
   ...:  
   ...:     if '--name' in sys.argv: 
   ...:         # Get position after name flag 
   ...:  
   ...:         # We need the position of the value after the flag, which should be the associated value. 
   ...:         name_index = sys.argv.index('--name') + 1 
   ...:  
   ...:         # Test that the arguments list is long enough. It will not be if the flag was provided without a value. 
   ...:         if name_index < len(sys.argv): 
   ...:             name = sys.argv[name_index] 
   ...:  
   ...:     if '--greeting' in sys.argv: 
   ...:         # Get position after greeting flag 
   ...:         greeting_index = sys.argv.index('--greeting') + 1 
   ...:         if greeting_index < len(sys.argv): 
   ...:             greeting = sys.argv[greeting_index] 
   ...:  
   ...:     # Call the function with the values as modified by the arguments. 
   ...:     say_it(greeting, name) 

Overwriting sys_argv.py

In [8]: !python3 sys_argv.py --help                                                                                                  
Usage: sys_argv.py --name <NAME> --greeting <GREETING>

In [9]: !python3 sys_argv.py --name Priyanka --greeting Hey                                                                          
Hey Priyanka
```
---

- The above approach is fraught with complication and potential bugs, as it fails to handle many situations. 
    - If a user misspells or miscapitalizes a flag, the flag is ignored with no useful feedback.
    - If they use commands that are not supported or try to use more than one value with a flag, once again the error is ignored.

- Luckily there are modules and packages designed for the creation of command-line tools. These packages provide frameworks to design the user interface for your module when running in a shell. Three popular solutions are `argparse`, `click`, and `python-fire`.
    - All three include ways to design required arguments, optional flags, and means to display help documentation.
    - The first, `argparse`, is part of the Python standard library, and the other two are third-party packages that need to be installed separately (using pip).

---

***Continued ...***
