---
layout: post
title: "[Python for DevOps] Pytest for DevOps!"
description: "This post contain notes from Chapter-8 'Pytest for DevOps' from the book, Python for DevOps!"
category: learning-python
tags: [DevOps, Python, Notes]
comments: false
---

August 10, 2020

Ok, this time I made a jump from *chapter 3*, to directly *chapter 8* in the book ***Python for DevOps***, because I needed to learn about writing tests/unitests in python.

When I say writing tests, I broadly mean *writing validation steps*, to check if everything is happening the intended way or not. And if not, then what kind of behaviour I'm receiving from my program, or infrastructure.<!-- break -->

*(**Note:** The notes below are the direct excerpts from the book, [Python For DevOps](https://learning.oreilly.com/library/view/python-for-devops/9781492057680/), compiled for the purpose of learning & memory.)*

---

> This validation can happen at every step of the way and when achieving important objectives.
>
> For example, if in the middle of a long list of steps to produce a deployment, a curl command is called to get an all-important file, do you think the build should continue if it fails? Probably not! curl has a flag that can be used to produce a nonzero exit status (--fail) if an HTTP error happens. That simple flag usage is a form of validation: ensure that the request succeeded, otherwise fail the build step.

This chapter talked about:
- the basics associated with testing in Python using the phenomenal `pytest` framework.
- then dives into some advanced features of the framework.
- finally goes into detail about the TestInfra project, a plug-in to pytest that can do system verification.

---

- `pytest` is a command-line tool that discovers Python tests and executes them.
    - It doesn’t force a user to understand its internals, which makes it easy to get started with. 

---

### Testing with Pytest!

- Create a python virtual environment (venv) named `testing`. And make sure `pytest` is installed & available in the command line.

```bash
$ python3 -m venv testing
$ source testing/bin/activate

$ pip3 install pytest
```

- Create a file called `test_basic.py`. It should look like this:

```python
def test_simple():
    assert True

def test_fails():
    assert False
```

- If pytest runs without any arguments, it should show a pass and a failure.

```bash
(testing) $ pytest

====================== test session starts =======================
platform linux -- Python 3.8.2, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/priyankasaggu119/Desktop/.myhome/python-study
plugins: testinfra-2.1.0
collected 2 items                                                

test_basic.py .F                                           [100%]

============================ FAILURES ============================
___________________________ test_fails ___________________________

    def test_fails():
>       assert False
E       assert False

test_basic.py:5: AssertionError
==================== short test summary info =====================
FAILED test_basic.py::test_fails - assert False
================== 1 failed, 1 passed in 0.13s ===================
```

- The output is beneficial from the start:
    - it displays how many tests were collected.
    - how many of them passed.
    - and which one failed—including its line number.

> The default output from pytest is handy, but it might be too verbose. You can control the amount of output with configuration, reducing it with the `-q` flag.

- There was no need to create a class to include the tests; functions were discovered and ran correctly. A test suite can have a mix of both, and the framework works fine in such an environment.

---

These are conventions that will allow the tool to discover tests:

    - The testing directory needs to be named `tests`.

    - Test files need to be prefixed with `test`. For example, `test_basic.py`, or suffixed with `test.py`.

    - Test functions need to be prefixed with `test_`, for example, `def testsimple():`.

    - Test classes need to be prefixed with `Test`; for example, `class TestSimple`.

    - Test methods follow the same conventions as functions, prefixed with `test_`; for example, `def test_method(self):`.

- Because prefixing with `test_` is a requirement for automatic discovery and execution of tests, it allows introducing helper functions and other nontest code with different names, so that they get excluded automatically.

---

### Differences with `unittest`!

Python already comes with a set of utilities and helpers for testing, and they are part of the `unittest` module. It is useful to understand how `pytest` is different and why it is highly recommended.

- [`unitest`] The `unittest` module forces the use of classes and class inheritance. For an experienced developer who understands object-oriented programming and class inheritance, this shouldn’t be a problem, but for beginners, it is an obstacle. Using classes and inheritance shouldn’t be a requisite for writing basic tests!

- [`unitest`] Part of forcing users to inherit from unittest.TestCase is that you are required to understand (and remember) most of the assertion methods that are used to verify results.

- [`pytest`] With `pytest`, there is a single assertion helper that can do it all: `assert`.

- [`pytest`] `pytest` allows you to use assert exclusively and does not force you to use any of the above. Moreover, it does allow you to write tests using unittest, and it even executes them. We strongly advise against doing that and suggest you concentrate on just using plain asserts.

- [`pytest`] Not only is it easier to use plain asserts, but pytest also provides a rich comparison engine on failures (more on this in the next section).

---

### Pytest Features!

Hooks are an advanced feature of pytest that you might not need at all, but it is useful to understand that the framework can be flexible enough to accommodate different requirements.

Here, we will talk about how to extend the framework.
- why using `assert` is so valuable.
- how to `parametrize` tests to reduce repetition.
- how to make helpers with `fixtures`, and how to use the built-in ones.

#### conftest.py

- `conftest.py` file is used to hold hooks, fixtures, and helpers for those fixtures. Those fixtures can then be used within tests if declared as arguments.

*(I'll discuss about fixtures later in the blog!)*

> It makes sense to add fixtures and helpers to this file when more than one test module will use it. If there is only a single test file, or if only one file is going to make use of a fixture or hook, there is no need to create or use a conftest.py file. Fixtures and helpers can be defined within the same file as the test and behave the same.

- The only condition for loading a `conftest.py` file is to be present in the tests directory and match the name correctly.

---

### Difference between using direct `assert` and using pytest `assert`.

```python
>>> assert "using assert for errors" == "using asert for errors"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError
```

Here, it is hard to tell the error/issue without spending some time looking at those two long lines closely.

Now let's look at the same `assert` inside a test file.

```python
def test_long_files():
	assert "using assert for errors" == "using asert for errors"
```

```bash
(testing) $ pytest test_long_lines.py

====================== test session starts =======================
platform linux -- Python 3.8.2, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/priyankasaggu119/Desktop/.myhome/python-study
plugins: testinfra-2.1.0
collected 1 item                                                 

test_ll.py F                                               [100%]

============================ FAILURES ============================
________________________ test_long_files _________________________

    def test_long_files():
>       assert "using assert for errors" == "using asert for errors"
E       AssertionError: assert 'using assert for errors' == 'using asert for errors'
E         - using asert for errors
E         + using assert for errors
E         ?        +

test_ll.py:2: AssertionError
==================== short test summary info =====================
FAILED test_ll.py::test_long_files - AssertionError: assert 'us...
======================= 1 failed in 0.12s ========================

```

This time, telling *where the error is?* is tremendously easier. Not only does it tell you it fails, but it points to exactly where the failure is.

The example is a simple assert with a long string, but the framework handles other data structures like lists and dictionaries without a problem.

---

### Parametrization

**Parametrization** is one of the features which become clear once you find yourself writing very similar tests that had minor changes in the inputs but are testing the same thing.

Take, for example, this class that is testing a function that returns `True` if a string is implying a truthful value. The `string_to_bool` is the function under test.

```python
from my_module import string_to_bool

class TestStringToBool(object):

    def test_it_detects_lowercase_yes(self):
        assert string_to_bool('yes')

    def test_it_detects_odd_case_yes(self):
        assert string_to_bool('YeS')

    def test_it_detects_uppercase_yes(self):
        assert string_to_bool('YES')

    def test_it_detects_positive_str_integers(self):
        assert string_to_bool('1')

    def test_it_detects_true(self):
        assert string_to_bool('true')

    def test_it_detects_true_with_trailing_spaces(self):
        assert string_to_bool('true ')

    def test_it_detects_true_with_leading_spaces(self):
        assert string_to_bool(' true')
```

See how all these tests are evaluating the same result from similar inputs? 

This is where *parametrization* shines because it can group all these values and pass them to the test. Thus, it can effectively reduce them to a single test.

```python
import pytest
from my_module import string_to_bool

true_values = ['yes', '1', 'Yes', 'TRUE', 'TruE', 'True', 'true']

class TestStrToBool(object):

    @pytest.mark.parametrize('value', true_values)
    def test_it_detects_truish_strings(self, value)
        assert string_to_bool(value)
```

There are a couple of things happening here.
- first `pytest` is imported (the framework) to use the `pytest.mark.parametrize` module.
- then `true_values` is defined as a (list) variable of all the values to use that should evaluate the same.
- finally, it replaces all the test methods to a single one.
- The test method uses the `parametrize` decorator, which defines two arguments.
    - first is a string, `value`.
    - second is the name of the list `true_values`, defined previously.

- Increase the verbosity of the test by adding `-v` flag, and the output will include the values used in each iteration of the single test in brackets.

```bash
(testing) $ pytest test_something.py -v

================================ test session starts ================================
platform linux -- Python 3.8.2, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/priyankasaggu119/Desktop/.myhome/python-study
plugins: testinfra-2.1.0
collected 7 items                                                                   

test_something.py::TestStrToBool::test_it_detects_truish_strings[yes] PASSED  [ 14%]
test_something.py::TestStrToBool::test_it_detects_truish_strings[1] PASSED    [ 28%]
test_something.py::TestStrToBool::test_it_detects_truish_strings[Yes] PASSED  [ 42%]
test_something.py::TestStrToBool::test_it_detects_truish_strings[TRUE] PASSED [ 57%]
test_something.py::TestStrToBool::test_it_detects_truish_strings[TruE] PASSED [ 71%]
test_something.py::TestStrToBool::test_it_detects_truish_strings[True] PASSED [ 85%]
test_something.py::TestStrToBool::test_it_detects_truish_strings[true] PASSED [100%]

================================= 7 passed in 0.04s =================================
```

### Fixtures!

*(Refer the official docs for fixtures (here.)[https://docs.pytest.org/en/latest/fixture.html])*

Pytest `fixtures` are like little helpers that can get injected into a test. Regardless of whether you are writing a single test function or a bunch of test methods, fixtures can be used in the same way. 

If they aren’t going to be shared among other test files, it is fine to define them in the same test file; otherwise they can go into the `conftest.py` file.

Fixtures, just like helper functions, can be almost anything you need for a test, from simple data structures that get pre-created to more complex ones like setting a database for a web application.

> These helpers can also have a defined scope. They can have specific code that cleans up for every test method, class, and module, or even allows setting them up once for the whole test session. By defining them in a test method (or test function), you are effectively getting the fixture injected at runtime.

#### Fixtures as Function arguments

- Test functions can receive fixture objects by naming them as an input argument. 
- For each argument name, a fixture function with that name provides the fixture object. 
- Fixture functions are registered by marking them with `@pytest.fixture`.

```python
# content of ./test_smtpsimple.py
import pytest


@pytest.fixture
def smtp_connection():
    import smtplib

    return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)


def test_ehlo(smtp_connection):
    response, msg = smtp_connection.ehlo()
    assert response == 250
    assert 0  # for demo purposes
```

- Here, the `test_ehlo` needs the `smtp_connection` fixture value. `pytest` will discover and call the `@pytest.fixture` marked `smtp_connection` fixture function.

```bash
(testing) $ pytest test_smtpsimple.py 

================================ test session starts ================================
platform linux -- Python 3.8.2, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/priyankasaggu119/Desktop/.myhome/python-study
plugins: testinfra-2.1.0
collected 1 item                                                                    

test_smtpsimple.py F                                                          [100%]

===================================== FAILURES ======================================
_____________________________________ test_ehlo _____________________________________

smtp_connection = <smtplib.SMTP object at 0x7fe07285e7f0>

    def test_ehlo(smtp_connection):
        response, msg = smtp_connection.ehlo()
        assert response == 250
>       assert 0  # for demo purposes
E       assert 0

test_smtpsimple.py:14: AssertionError
============================== short test summary info ==============================
FAILED test_smtpsimple.py::test_ehlo - assert 0
================================= 1 failed in 0.82s =================================
```

In the failure traceback, we see that the test function was called with a `smtp_connection` argument, the `smtplib.SMTP()` instance created by the fixture function. The test function fails on our deliberate `assert 0`.

Here is the exact protocol used by `pytest` to call the test function this way:
    - `pytest` finds the test `test_ehlo` because of the `test_` prefix. The test function needs a function argument named `smtp_connection`. A matching fixture function is discovered by looking for a fixture-marked function named `smtp_connection`.
    - `smtp_connection()` is called to create an instance.
    - `test_ehlo(<smtp_connection instance>)` is called and fails in the last line of the test function.

#### Built-in Fixtures

- To verify the full list of available built-in fixtures, run the following command.

```bash
$ (testing) pytest  -q --fixtures
```

- There are two fixtures that we use a lot: `monkeypatch` and `capsys`.

- `capsys` captures any stdout or stderr produced in a test, in a tupe `(stdout, stderr)`.

- These are two test functions that verify the output produced on stderr and stdout, respectively.

```python
import sys

def stderr_logging():
    sys.stderr.write('stderr output being produced')

def stdout_logging():
    sys.stdout.write('stdout output being produced')

def test_verify_stderr(capsys):
    stderr_logging()
    out, err = capsys.readouterr()
    assert out == ''
    assert err == 'stderr output being produced'

def test_verify_stdout(capsys):
    stdout_logging()
    out, err = capsys.readouterr()
    assert out == 'stdout output being produced'
    assert err == ''
```

- The `capsys` fixture handles all the patching, setup, and helpers to retrieve the `stderr` and `stdout` produced in the test.
    - The content is reset for every test, which ensures that the variables populate with the correct output.

---

- `monkeypatch` is probably the fixture that we use the most.

> When testing, there are situations where the code under test is out of our control, and patching needs to happen to override a module or function to have a specific behavior. There are quite a few patching and mocking libraries (mocks are helpers to set behavior on patched objects) available for Python, but `monkeypatch` is good enough that you might not need to install a separate library to help out.

- The following function runs a system command to capture details from a device, then parses the output, and returns a property (the `ID_PART_ENTRY_TYPE` as reported by `blkid`):

```python
import subprocess

def get_part_entry_type(device):
    """
    Parses the ``ID_PART_ENTRY_TYPE`` from the "low level" (bypasses the cache)
    output that uses the ``udev`` type of output.
    """
    stdout = subprocess.check_output(['blkid', '-p', '-o', 'udev', device])
    for line in stdout.split('\n'):
        if 'ID_PART_ENTRY_TYPE=' in line:
            return line.split('=')[-1].strip()
    return ''

def test_parses_id_entry_type(monkeypatch):
    monkeypatch.setattr(
        'subprocess.check_output',
        lambda cmd: '\nID_PART_ENTRY_TYPE=aaaaa')
    assert get_part_entry_type('/dev/sda') == 'aaaa'
```

- The `setattr` call sets the attribute on the patched callable (`check_output` in this case).
- It patches it with a lambda function that returns the one interesting line. Since the `subprocess.check_output` function is not under our direct control, and the `get_part_entry_type` function doesn’t allow any other way to inject the values, patching is the only way.

```bash
(testing) $ pytest test_monkeypath.py

================================ test session starts ================================
platform linux -- Python 3.8.2, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/priyankasaggu119/Desktop/.myhome/python-study
plugins: testinfra-2.1.0
collected 1 item                                                                    

test_monkeypath.py F                                                          [100%]

===================================== FAILURES ======================================
_____________________________ test_parses_id_entry_type _____________________________

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x7fc9407b0670>

    def test_parses_id_entry_type(monkeypatch):
        monkeypatch.setattr(
            'subprocess.check_output',
            lambda cmd: '\nID_PART_ENTRY_TYPE=aaaaa')
>       assert get_part_entry_type('/dev/sda') == 'aaaa'
E       AssertionError: assert 'aaaaa' == 'aaaa'
E         - aaaa
E         + aaaaa
E         ?     +

test_monkeypath.py:18: AssertionError
============================== short test summary info ==============================
FAILED test_monkeypath.py::test_parses_id_entry_type - AssertionError: assert 'aaa...
================================= 1 failed in 0.12s =================================
```

---

So, till here, We have discussed all writing basic `pytest` tests, then exploring the advanced features provided by the module like helper function hooks, `conftest.py` file, parametrization, custom & built-in `fixtures` and lots of supporting examples.

I'm breaking it here, & will cover the *Infrastructure Testing* using `pytest` module & plugins, in the next blog!
