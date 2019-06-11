# lscvmdbg

A debugger for lscvm and lscasm language compiler&documentation in cddc 2019

Use `./lscvm-qh a` to see the stack after every instruction for the actual vm

Use `python2 lscvmdbg.py` for a python interpreter and debugger

Use `python lscasm_compiler.py [lscasm file]` to compile

## Debugger

Features:
* Use `h` in debugger to list debugger instructions 
* Lscasm that is more readable then reading single letters
* Stack view and code view with *partially* working predictive execution(uses current stack not future stack)

## Quine

genstack puts a string on the stack

qhprintstack prints the stack from a certain offset

qhgenstack prints code that generates the stack from a certain offset

combined is combining all of these

quine is the final quine in lscvm

## ToDo

* lscasm-\>lscvm
  * Escape strings
  * Implement some sort of variable system
  * Implement some sort of function system
* lscvm-\>lscasm
  * Labels
  * Simplifying pushing large numbers(i.e. `jjM` -\> `Push 81`)

