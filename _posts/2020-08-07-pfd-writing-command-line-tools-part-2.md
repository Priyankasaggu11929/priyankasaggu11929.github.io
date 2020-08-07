---
layout: post
title: "[Python for DevOps] Working with the Command Line - Part 2!"
description: "This post contain notes from Chapter-3 'Working with the Command Line' from the book, Python for DevOps!"
category: learning-python
tags: [DevOps, Python, Notes]
comments: false
---

August 07, 2020

In continuation with [my previous book notes from the Chapter 3](https://priyankasaggu11929.github.io/learning-python/2020/08/07/pfd-working-with-the-command-line.md.html), *Working with the command line*, from the book *Python for DevOps!*

So, far... 

- I learnt how to interact with the system & shell using Python, with the help of `sys`, `os`, & `subprocess` modules. 
- Then I learnt about how to separate *command line python script calls* from the *module import* invocation, using the conditional check with global `name` variable (i.e. if '__name__' == '__main__').
- And then I started with the very basics of writing *command line tools*, using the `sys.argv` attribute which creats a list of arguments passed while invoking the script. 
- And finally that was followed by writing a small python argument parser using the same `sys.argv` module.

Now, the current approach of writing command line tools using just, `sys.argv` attribute contains lots of complications & potential bugs, which I briefly discussed [in the end of my last post](https://priyankasaggu11929.github.io/learning-python/2020/08/07/pfd-working-with-the-command-line.md.html).

- Therefore, moving forward, here I will write notes around what I learnt about the three popular python modules solutions for writing command line tools.
    1. `argparse`
    2. `click`
    3. `python-fire`

---

### Using `argparse`!

> `argparse` abstracts away many of the details of parsing arguments. With it, you design your command-line user interface in detail, defining commands and flags along with their help messages. 
>
>    - It uses the idea of parser objects, to which you attach commands and flags.
>    - The parser then parses the arguments, and you use the results to call your code. 
>    - You construct your interface using `ArgumentParser` objects that parse user input for you.
>
>    ```python
>    if __name__ == '__main__':
>        parser = argparse.ArgumentParser(description='Maritime control')
>    ```
>
>    - Then you add position-based commands or optional flags to the parser using the `add_argument` method.
>        - The first argument to this method is the name of the new argument (command or flag).
>        - If the name begins with a `dash (-- or -)`, it is treated as an optional flag argument; otherwise it is treated as a position-dependent command.     
>    - The parser creates a parsed-arguments object, with the arguments as attributes that you can then use to access input.

```python
#!/usr/bin/env python
"""
Command-line tool using argparse
"""
import argparse


if __name__ == '__main__':

    # Create the parser object, with its documentation message.
    parser = argparse.ArgumentParser(description='Echo your input')

    # Add a position-based command with its help message.
    parser.add_argument('message',
                        help='Message to echo')

    # Add an optional argument.
    # `action=store_true` stores the optional argument as a boolean value.
    parser.add_argument('--twice', '-t',
                        help='Do it twice',
                        action='store_true')

    # Use the parser to parse the arguments.
    args = parser.parse_args()

    # Access the argument values by name. The optional argument’s name has the -- removed.
    print(args.message)
    if args.twice:
        print(args.message)
```

- And when invoked from command line,

```bash
$ python3 simple_parse.py hello --twice                                                                                      
hello
hello

$ python3 simple_parse.py --help                                                                                             
usage: simple_parse.py [-h] [--twice] message

Echo your input

positional arguments:
  message      Message to echo

optional arguments:
  -h, --help   show this help message and exit
  --twice, -t  Do it twice
```

> Many command-line tools use nested levels of commands to group command areas of control. Think of `git`. It has top-level commands, such as `git stash`, which have separate commands under them, such as `git stash pop`. 

- With `argparse`, you create subcommands by creating `subparsers` under your main parser. You can create a hierarchy of commands using subparsers.

*(Now we're picking up an example python problem `implement a maritime application that has commands for ships and sailors` which will later be used to learn all the other 2 modules as well. So, the comparision will be much easier!)*

```python
#!/usr/bin/env python
"""
Command-line tool using argparse
"""
import argparse

def sail():
    ship_name = 'Your ship'
    print(f"{ship_name} is setting sail")

def list_ships():
    ships = ['John B', 'Yankee Clipper', 'Pequod']
    print(f"Ships: {','.join(ships)}")

def greet(greeting, name):
    message = f'{greeting} {name}'
    print(message)

if __name__ == '__main__':

    # Create the top-level parser.
    parser = argparse.ArgumentParser(description='Maritime control')

    # Add a top-level argument that can be used along with any command under this parser’s hierarchy.
    parser.add_argument('--twice', '-t',
                        help='Do it twice',
                        action='store_true')

    # Create a subparser object to hold the subparsers. The dest is the name of the attribute used to choose a subparser.
    subparsers = parser.add_subparsers(dest='func')

    # Add a subparser for ships.
    ship_parser =  subparsers.add_parser('ships',
                                         help='Ship related commands')

    # Add a command to the ships subparser. The choices parameter gives a list of possible choices for the command.
    ship_parser.add_argument('command',
                             choices=['list', 'sail'])

    # Add a subparser for sailors.
    sailor_parser = subparsers.add_parser('sailors',
                                          help='Talk to a sailor')

    # Add a required positional argument to the sailors subparser.
    sailor_parser.add_argument('name',
                               help='Sailors name')
    sailor_parser.add_argument('--greeting', '-g',
                               help='Greeting',
                               default='Ahoy there')

    args = parser.parse_args()

    #  Check which subparser is used by checking the `func` value.
    if args.func == 'sailors':
        greet(args.greeting, args.name)
    elif args.command == 'list':
        list_ships()
    else:
        sail()
```

- again, when invoked from command line

```bash
$ python3 argparse_example.py --help                                                                                         
usage: argparse_example.py [-h] [--twice] {ships,sailors} ...

Maritime control

positional arguments:
  {ships,sailors}
    ships          Ship related commands
    sailors        Talk to a sailor

optional arguments:
  -h, --help       show this help message and exit
  --twice, -t      Do it twice

$ python3 argparse_example.py ships --help                                                                                   
usage: argparse_example.py ships [-h] {list,sail}

positional arguments:
  {list,sail}

optional arguments:
  -h, --help   show this help message and exit
```

> As you can see, argparse gives you a lot of control over your command-line interface. You can design a multilayered interface with built-in documentation with many options to fine-tune your design. Doing so takes a lot of work on your part, however, so let’s look at some easier options.

---

**Before moving forward to further modules, lets first learn a bit about `Function Decorators`!**

- `Python decorators` are a special syntax for functions which take other functions as arguments. Python functions are objects, so any function can take a function as an argument. The decorator syntax provides a clean and easy way to do this. 

- The basic format of a decorator is:

```ipython3
In [2]: def some_decorator(wrapped_function):
   ...:     def wrapper():
   ...:         print('Do something before calling wrapped function')
   ...:         wrapped_function()
   ...:         print('Do something after calling wrapped function')
   ...:     return wrapper
```

- You can define a function and pass it as an argument to this function:

```ipython3
In [3]: def foobat():
   ...:     print('foobat')
   ...:

In [4]: f = some_decorator(foobat)

In [5]: f()
Do something before calling wrapped function
foobat
Do something after calling wrapped function
```

- The decorator syntax simplifies this by indicating which function should be wrapped by decorating it with `@decorator_name`. Here is an example using the decorator syntax with the above `some_decorator` function:

```ipython3
In [6]: @some_decorator
   ...: def batfoo():
   ...:     print('batfoo')
   ...:

In [7]: batfoo()
Do something before calling wrapped function
batfoo
Do something after calling wrapped function
```

- Now you call your wrapped function using its name rather than the decorator name, which means:
    - Not as first, `f = some_decorator(foobat)` and then `f()`.
    - But directly, `footbat()`.

- Pre-built functions intended as decorators are offered both as part of the Python Standard Library (`staticMethod`, `classMethod`) and as part of third-party packages, such as `Flask` and `Click`.

*(And the reason that `Click` module offers pre-built functions as decorators, we learnt about decorators first before directly moving to `click` module!)*

---

### Using `click`

> The `click` package was first developed to work with web framework flask. It uses `Python function decorators` to bind the command-line interface directly with your functions. Unlike `argparse`, `click` interweaves your interface decisions directly with the rest of your code.

```python
#!/usr/bin/env python
"""
Simple Click example
"""
import click

@click.command()
@click.option('--greeting', default='Hiya', help='How do you want to greet?')
@click.option('--name', default='Tammy', help='Who do you want to greet?')
def greet(greeting, name):
    print(f"{greeting} {name}")

if __name__ == '__main__':
    greet()
```

```python
$ python3 simple_click.py --greeting Heyya --name Priyanka                                                                   
Heyya Priyanka

$ python3 simple_click.py --help                                                                                             
Usage: simple_click.py [OPTIONS]

Options:
  --greeting TEXT  How do you want to greet?
  --name TEXT      Who do you want to greet?
  --help           Show this message and exit.
```

- `click.command` indicates that a function should be exposed to command-line access.
- `click.option` adds an argument to the command-line, automatically linking it to the function parameter of the same name (`--greeting to greet` and `--name to name`).

- And let's look a more complex `click` implementation using `click.group` for the same *Ships & Sailors* problem!


```python
#!/usr/bin/env python
"""
Command-line tool using click
"""
import click

# Create a top-level group under which other groups and commands will reside.
@click.group()

# Create a function to act as the top-level group. The click.group method transforms the function into a group.
def cli():
    pass

# Create a group to hold the ships commands.
@click.group(help='Ship related commands')
def ships():
    pass

# Add the ships group as a command to the top-level group. Note that the cli function is now a group with an add_command method.    
cli.add_command(ships)

# Add a command to the ships group. Notice that ships.command is used instead of `click.command`.
@ships.command(help='Sail a ship')
def sail():
    ship_name = 'Your ship'
    print(f"{ship_name} is setting sail")

@ships.command(help='List all of the ships')
def list_ships():
    ships = ['John B', 'Yankee Clipper', 'Pequod']
    print(f"Ships: {','.join(ships)}")

# Add a command to the cli group.    
@cli.command(help='Talk to a sailor')
@click.option('--greeting', default='Ahoy there', help='Greeting for sailor')
@click.argument('name')
def sailors(greeting, name):
    message = f'{greeting} {name}'
    print(message)

if __name__ == '__main__':

    # Call the top-level group.     
    cli()
```

- when invoked from command line,

```bash
$ python3 click_example.py --help                                                                                            
Usage: click_example.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  sailors  Talk to a sailor
  ships    Ship related commands

$ python3 click_example.py ships --help                                                                                      
Usage: click_example.py ships [OPTIONS] COMMAND [ARGS]...

  Ship related commands

Options:
  --help  Show this message and exit.

Commands:
  list-ships  List all of the ships
  sail        Sail a ship
```

>  The `click` approach certainly requires less code, almost half in these examples. The user interface (UI) code is interspersed throughout the whole program; it is especially important when creating functions that solely act as groups. 
> 
> If you have a complex program, with a complex interface, you should try as best as possible to isolate different functionality. By doing so, you make individual pieces easier to test and debug. In such a case, you might choose `argparse` to keep your interface code separate.

---

***Now again, before moving forward further to the final module here, let's first discuss about `Python Classes`!***

- A class definition starts with the keyword `class` followed by the `class name` and `parentheses`, like, `class MyClass():`.
- Attributes and method definitions follow in the indented code block.
- All methods of a class recieve as their first parameter a copy of the instantiated class object. 
- And by convention, this copy of the instanitated class object is refered to as `self`!

```jupyter
In [1]: class MyClass():
   ...:     def some_method(self):
   ...:         print(f"Say hi to {self}")
   ...:

In [2]: myObject = MyClass()

In [3]: myObject.some_method()
Say hi to <__main__.MyClass object at 0x1056f4160>
```

- Every class has an `init` method. 
- When the class is instantiated, this method is called. If you do not define this method, it gets a default one, inherited from the Python base object class.

```jupyter
In [4]: MyClass.__init__
Out[4]: <slot wrapper '__init__' of 'object' objects>
```

- Generally you define an object’s attributes in the `init` method.

```jupyter
In [5]: class MyOtherClass():
   ...:     def __init__(self, name):
   ...:         self.name = name
   ...:

In [6]: myOtherObject = MyOtherClass('Sammy')

In [7]: myOtherObject.name
Out[7]: 'Sammy'
```

---

### Using `fire`!

- Now's the time to take a step farther down the road of making a command-line tool with minimal UI code.
- The fire package uses introspection of your code to create interfaces automatically. If you have a simple function you want to expose, you call `fire.Fire` with it as an argument.

```python
#!/usr/bin/env python
"""
Simple fire example
"""
import fire

def greet(greeting='Hiya', name='Priyanka'):
    print(f"{greeting} {name}")

if __name__ == '__main__':
    fire.Fire(greet)
```

- and when invoked, gives:

```bash
$ ./simple_fire.py --help

NAME
    simple_fire.py

SYNOPSIS
    simple_fire.py <flags>

FLAGS
    --greeting=GREETING
    --name=NAME
```

- In simple cases, you can expose multiple methods automatically by invoking fire with no arguments. fire creates a command from each function and documents automatically.

```python
#!/usr/bin/env python
"""
Simple fire example
"""
import fire

def greet(greeting='Hiya', name='Tammy'):
    print(f"{greeting} {name}")

def goodbye(goodbye='Bye', name='Tammy'):
    print(f"{goodbye} {name}")

if __name__ == '__main__':
    fire.Fire()
```

- And now back to oue *Ships & Sailors example*, To mimic this nest command interface, you need to define classes with the structure of the interface you want to expose. (And that is the reason why we learnt about python classes above! :) )


```python
#!/usr/bin/env python
"""
Command-line tool using fire
"""
import fire

# Define a class for the ships commands.
class Ships(): 
    def sail(self):
        ship_name = 'Your ship'
        print(f"{ship_name} is setting sail")

    def list(self):
        ships = ['John B', 'Yankee Clipper', 'Pequod']
        print(f"Ships: {','.join(ships)}")

# sailors has no subcommands, so it can be defined as a function.
def sailors(greeting, name): 
    message = f'{greeting} {name}'
    print(message)

# Define a class to act as the top group. Add the sailors function and the Ships as attributes of the class.
class Cli(): 

    def __init__(self):
        self.sailors = sailors
        self.ships = Ships()

if __name__ == '__main__':

    # Call fire.Fire on the class acting as the top-level group.
    fire.Fire(Cli) 
```

- and when invoked, it automatically generated documentation at the top level represents the `Ships class as a group`, and the `sailors command as a command`. 

```bash
$ ./fire_example.py

NAME
    fire_example.py

SYNOPSIS
    fire_example.py GROUP | COMMAND

GROUPS
    GROUP is one of the following:

     ships

COMMANDS
    COMMAND is one of the following:

     sailors
(END)
```
- and you can call the commands and subcommands as expected.

```bash
$ ./fire_example.py ships sail
Your ship is setting sail
$ ./fire_example.py ships list
Ships: John B,Yankee Clipper,Pequod
$ ./fire_example.py sailors Hiya Karl
Hiya Karl
```
---

> You have now run the gamut in command-line tool building libraries, from the very hands-on `argparse`, to the less verbose `click`, and lastly to the minimal `fire`.>
> So which one should you use? 
>
> We recommend 
> - `click` for most use cases. It balances ease and control. 
> - In the case of complex interfaces where you want to separate the UI code from business logic, `argparse` is the way to go. 
> - Moreover, if you need to access code that does not have a command-line interface quickly, `fire` is right for you.


***Before we end fire module section, I have a moment to share while I was learning***

For about 30 minutes or so, I was trying to run the above `fire` module's, code snippets in my interpreter. And everytime, it was throwing this same error to me `AttributeError: module 'fire' has no attribute 'Fire'`.

I did all possible tries in the terminal (atleast that's what I believed at that time.)

And then I finally looked on internet for help, and I landed at this [github issue](https://github.com/google/python-fire/issues/165.)

Someone just like me, was trying to run fire module in their python interpreter and getting the same error, and (thankfully) he cared to raise this as an issue.

But to both our surprise (and to many others), it was nothing of an actual error but a lame mistake we did. (And the man who raised, he himself figured out the issue as well. Smart he is!)

So, We named the script itself as `fire.py`. And thus, everytime, when we wrote `import fire`, it was importing the local script `fire.py`, rather the installed python module. XD

---

### Implementing Plug-ins

> Once you’ve implemented your application’s command-line user interface, you might want to consider a `plug-in` system. Plug-ins are pieces of code supplied by the user of your program to extend functionality. 

- You could write a tool that handles walking a filesystem and allows a user to provide plug-ins to operate on its contents. 
    - A key part of any plug-in system is plug-in discover. 
    - Your program needs to know what plug-ins are available to load and run.

- Here is a simple application that discovers and runs plug-ins. It uses a user-supplied prefix to search for, load, and run plug-ins:

```python
#!/usr/bin/env python
import fire
import pkgutil
import importlib

def find_and_run_plugins(plugin_prefix):
    plugins = {}

    # Discover and Load Plugins
    print(f"Discovering plugins with prefix: {plugin_prefix}")

    # `pkgutil.iter_modules` returns all modules available in the current `sys.path`.
    for _, name, _ in  pkgutil.iter_modules(): 

        # Check if the module uses our plug-in prefix.
        if name.startswith(plugin_prefix): 

            # Use `importlib` to load the module, saving it in a dict for later use.
            module = importlib.import_module(name) 
            plugins[name] = module

    # Run Plugins
    for name, module in plugins.items():
        print(f"Running plugin {name}")

        # Call the run method on the plug-in.
        module.run()  

if __name__ == '__main__':
    fire.Fire()
```

- Now, Let's say, we have 2 files with the names, `foo_plugin-1.py` & `foo_pluging-2.py` respectively, with the following code snippets.

```python
# File `foo_plugin-1.py`
def run():
    print("Running plugin A")
```

```python
# File `foo_plugin-2.py`
def run():
    print("Running plugin B")
```

- You can discover and run them with our plugin application:

```bash
$ ./simple_plugins.py find_and_run_plugins foo_plugin
Running plugin foo_plugin_a
Running plugin A
Running plugin foo_plugin_b
Running plugin B
```


