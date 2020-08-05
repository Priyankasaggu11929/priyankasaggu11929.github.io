---
layout: post
title: "[Python for DevOps] Automating Files and the Filesystem"
description: "Notes from Chapter 2 of the book, Python for DevOps, on automating files & filesystem."
category: learning-python
tags: [DevOps, Python, Notes]
comments: false
---

August 05, 2020

Moving forward in the Book "Python for DevOps", yesterday I finished the second chapter, *Automating Files & the Filesystem!*

And I covered the following topics:

- [X] Using Regular Expressions to Search Text
- [X] Dealing with Large Files
- [X] Encrypting Text
- [X] The os Module
- [X] Managing Files and Directories Using os.path
- [X] Walking Directory Trees Using os.walk
- [X] Paths as Objects with Pathlib

---

I already had noted down couple of points, around reading & writing files in Python, in the last post. So, extending it more here,

- Apart from the `csv` module, the `Pandas` package is also a mainstay in data science world when it comes to processing large datasets.

> It includes a data structure, the pandas.DataFrame, which acts like a data table, similar to a very powerful spreadsheet. If you have table-like data on which you want to do statistical analysis or that you want to manipulate by rows and columns, DataFrames is the tool for you.

```python
import pandas as pd

df = pd.read_csv('sample-data.csv')

type(df)
pandas.core.frame.DataFrame
```
---

> [DEALING WITH SMALL FILES] 
>
> If the files contain data that can be processed one line at a time, the task is easy with Python. 
>
> Rather than loading the whole file into memory as you have done up until now, you can read one line at a time, process the line, and then move to the next. **The lines are removed from memory automatically by Python’s garbage collector, freeing up memory.**

- Python automatically allocates and frees memory. **Garbage collection** is one means of doing this. The Python garbage collector can be controlled using the gc package, though this is rarely needed.

- If you have a large file and you want to correct the line endings to fit your current OS, you can open the file, read one line at a time, and save it to a new file. Python handles the line-ending translation for you.

```python
with open('big-data.txt', 'r') as source_file:
     with open('big-data-corrected.txt', 'w') as target_file:
         for line in source_file:
             target_file.write(line)
```

- A similar way to handle the above problem using `generator` function, especially if it requires to parse the multiples files a single line at a time.

```python
def line_reader(file_path):
     with open(file_path, 'r') as source_file:
         for line in source_file:
             yield line

reader = line_reader('big-data.txt')

with open('big-data-corrected.txt', 'w') as target_file:
     for line in reader:
         target_file.write(line)
```

> If you do not or cannot use line endings as a means of breaking up your data, as in the case of a large binary file, you can read your data in chunks. You pass the number of bytes read in each chunk to the file objects read method. When there is nothing left to read, the expression returns an empty string.
>
> ```python
> with open('bb141548a754113e.jpg', 'rb') as source_file:
>     while True:
>         chunk = source_file.read(1024)
>         if chunk:
>             process_data(chunk)
>         else:
>             break
> ```

---

- There are many times you need to encrypt text to ensure security. In addition to Python’s built-in package `hashlib`, there is a widely used third-party package called `cryptography`

> To be secure, user passwords must be stored encrypted. A common way to handle this is to use a one-way function to encrypt the password into a bit string, which is very hard to reverse engineer. Functions that do this are called hash functions. In addition to obscuring passwords, hash functions ensure that documents sent over the web are unchanged during transmission. You run the hash function on the document and send the result along with the document. The recipient can then confirm that the value is the same when they hash the document. The hashlib includes secure algorithms for doing this, including SHA1, SHA224, SHA384, SHA512, and RSA’s MD5.

- Example demonstrating hasing a password using the MD5 algorithm.

```python
import hashlib

secret = "This is the password or document text"
bsecret = secret.encode()

m = hashlib.md5()
m.update(bsecret)

m.digest()

# OUTPUT
b' \xf5\x06\xe6\xfc\x1c\xbe\x86\xddj\x96C\x10\x0f5E'
```
- Notice that if your password or document is a string, you need to turn it into a binary string by using the `encode()` method.

---

> The cryptography library is a popular choice for handling encryption problems in Python. It is a third-party package, so you must install it with pip. Symmetric key encryption is a group of encryption algorithms based on shared keys. These algorithms include Advanced Encryption Algorithm (AES), Blowfish, Data Encryption Standard (DES), Serpent, and Twofish. A shared key is similar to a password that is used to both encrypt and decrypt text. The fact that both the creator and the reader of an encrypted file need to share the key is a drawback when compared to asymmetric key encryption, which we will touch on later. However, symmetric key encryption is faster and more straightforward, and so is appropriate for encrypting large files.

- `Fernet` is an implementation of AES algorithm.

```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()

key

# OUTPUT

b'q-fEOs2JIRINDR8toMG7zhQvVhvf5BRPx3mj5Atk5B8='
```
- The next step is to encrypt the data using the Fernet object.

```python
f = Fernet(key)

message = b"Secrets go here"

encrypted = f.encrypt(message)

encrypted

# OUTPUT

b'gAAAAABdPyg4 ... plhkpVkC8ezOHaOLIA=='
```
- And then you could decrypt the data using a Fernet object created with the same key.

```python
f = Fernet(key)

f.decrypt(encrypted)

# OUTPUT
b'Secrets go here'
```

---

> Asymmetric key encryption uses a pair of keys, one public and one private. The public key is designed to be widely shared, while a single user holds the private one. The only way you can decrypt messages that have been encrypted using your public key is by using your private key. This style of encryption is widely used to pass information confidentially both on local networks and across the internet. One very popular asymmetric key algorithm is **Rivest-Shamir-Adleman (RSA)**, which is widely used for communication across networks. 

- The cryptography library offers the ability to create public/private key pairs.

```python
from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives.asymmetric import rsa

private_key = rsa.generate_private_key(public_exponent=65537,
                                               key_size=4096,
                                               backend=default_backend())

private_key

# OUTPUT
<cryptography.hazmat.backends.openssl.rsa._RSAPrivateKey at 0x10d377c18>

public_key = private_key.public_key

public_key = private_key.public_key()

public_key

#OUTPUT
<cryptography.hazmat.backends.openssl.rsa._RSAPublicKey at 0x10da642b0>
```

- Now, use the public key to encrypt the message.

```python
message = b"More secrets go here"

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

encrypted = public_key.encrypt(message,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None)
```

- And, finally decrypt the message using the private key.

```python
decrypted = private_key.decrypt(encrypted,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None))

decrypted

# OUTPUT
b'More secrets go here'
```
---

- The `os` module handles many low-level operating system calls and attempts to offer a consistent interface across multiple operating systems, which is important if you think your application might run on both Windows and Unix-based systems. 
    - It does offer some operating-specific features (`os.O_TEXT` for Windows and `os.O_CLOEXEC` on Linux) that are not available across platforms. 

---

- [Managing Files and Directories Using os.path]

```python
In [1]: import os

In [2]: cur_dir = os.getcwd()

In [3]: cur_dir
Out[3]: '/Users/kbehrman/Google-Drive/projects/python-devops/samples/chapter4'

In [4]: os.path.split(cur_dir)
Out[4]: ('/Users/kbehrman/Google-Drive/projects/python-devops/samples',
         'chapter4')

In [5]: os.path.dirname(cur_dir)
Out[5]: '/Users/kbehrman/Google-Drive/projects/python-devops/samples'

In [6]: os.path.basename(cur_dir) 
Out[6]: 'chapter4'
```
---

- And I will repeat, I'm really loving the *IPython* interactive shell.
