# lscvmdbg

A debugger for lscvm in cddc 2019

Use `./lscvm-qh a` to see the stack after every instruction for the actual vm

Use `python2 lscvmdbg.py` for a python interpreter and debugger

## Debugger

Features:
* Use `h` in debugger to list debugger instructions 
* Lscasm that is more readable then reading single letters
* Stack view and code view with *partially* working predictive execution(uses current stack not future stack)

## ToDo

* lscasm-\>lscvm
  * Basic one to one op code translation
  * Labels
  * Simplifying pushing large numbers(i.e. `Push 81` -\> `jjM`)
  * Implement some sort of variable system
  * Implement some sort of function system
* lscvm-\>lscasm
  * Basic one to one op code translation
  * Labels
  * Simplifying pushing large numbers(i.e. `jjM` -\> `Push 81`)

