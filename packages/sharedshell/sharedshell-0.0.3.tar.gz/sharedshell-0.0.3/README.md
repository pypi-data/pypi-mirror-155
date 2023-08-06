# Shared shell for launching processes in Python

The purpose of this package is to provide a simple way to launch processes in Python but in the same shell. Only one shell is allocated and all the processes are launched in order. There is no need to allocate a different shell on each execution, and therefore it benefits from faster execution and a smaller memory footprint.

## Getting started

Installation via pip:

```shell
pip install sharedshell
```

Using it:

```python
from sharedshell import SharedShell

with SharedShell() as shell:
    print(shell.run('echo 1').stdout)
    print(shell.run('echo 2').stdout)
    print(shell.run('echo 3').stdout)
```

Output:
```shell
1
2
3
```

Benchmarking:

```shell
┌---------------------
| os.system
└--------------------
command: Mean +- std dev: 9.22 sec +- 2.33 sec
┌---------------------
| subprocess
└---------------------
command: Mean +- std dev: 7.48 sec +- 1.92 sec
┌---------------------
| sharedshell
└---------------------
command: Mean +- std dev: 2.11 sec +- 0.03 sec
```