# I'm Python

## What's `impython`?

`impython` is absolutely an interpreter for python based on the function `exec`. Besides, `impython` recognizes some magic commands.

## Why `impython`?

If any program is intended to call python and to get its results (either in form of returning values or making changes in OS), the most convenient method is to start a process of python and pass python commands to python interpreter via pipe. However, the way python interacts with pipe is wired. Python will NOT execute any commands until you close the stdin. But once you close the stdin, NO other commands can you write into stdin any more. 

By using `python -m impython`, now all issues are solved. Try this:

~~~ py
from subprocess import Popen, PIPE
with Popen(['python', '-m', 'impython'], stdin=PIPE) as f:
    f.stdin.write('print("hello world")'.encode())
    f.stdin.write('$exec'.encode())
    f.stdin.write('a = 1 / 0'.encode())
    f.stdin.write('$exec'.encode())
    f.stdin.write('$exit'.encode())
~~~

## How to `impython`?

An easy way is

~~~ sh
python -m pip install --upgrade pip
python -m pip install impython
~~~

A hard way is
~~~ sh
git clone https://gitee.com/junruoyu-zheng/impython.git
cd impython
python setup.py build
python setup.py install
~~~
