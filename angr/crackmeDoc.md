# This is the documentation of the angr ctf challenge for crackme

## Step-by-Step Guide


This document outlines the steps taken to identify and exploit a buffer overflow vulnerability
using tools like Ghidra, angr libray, virtual environment, and Python. Each step is critical
to understanding the target system, identifying the vulnerability, and creating a succesful
exploit.


### 1. Navigating Ghidra

**Description:**
Ghidra is a powerful open source reverse engineering tool that allows you to decompile and
analyze binary files.

* We first Launch Ghidra and created a new project

* We then import the target binary into the project

* We began to analyze the functions, and see if there is anything that seems interesting

* In the decompile section that shows the source code we found an important function


### 2. Analyzing the Code and File

While navigating the binary in Ghidra our objective was to identify potential vulernabilities,
we were able to inspect function calls and examine the calls to other functions.

**Observations:**
* There was a function call to _puts_ that prints out the string that shows that the user
guess the correct password. There was also another _puts_ call to print when the user guess
the password incorrectly. You see for this challenge we are prompeted to entered the corrcect
password in order to win. So by knowing where we need to go in memory it will allow us to
directly access the win conditon.

* This is when we _file_ the crackme file:
crackme: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked,
interpreter /lib64/ld-linux-x86-64.so.2,
BuildID[sha1]=a4e83e232e5b2c227eedee6f1c600956577a5cc9, for GNU/Linux 3.2.0, not stripped

* This is when we _checksec_ the crackme file:
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols               FORTIFY Fortified       Fortifiable     FILE
Partial RELRO   No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   71 Symbols      No    0               1               crackme


### 3. Identifying the Target Memory Address

**Description:**
Finding the memory address you want to return to after exploiting the buffer overflow is
critical for hijacking.

* **Analyze the Binary:** Using Ghidra to identify the memory address you want to redirect
execution to.

* **Record the Address:** This address will be used later in the payload to overwrite the
return address.

* **Desired Address:** This is the address in memory that we would want to return to

* **Wrong Address:** This is the address we don't want to go to, should be note down as well


### 4. The Python Program
```python
 import angr
 import claripy
 #import code

 # Establish the Angr Project
 target = angr.Project('crackme', main_opts = {'base_addr': 0x0})

 # Specify the desired address which means we have the correct input
 desired_adr = 0x1220


 # Specify the address which if it executes means we don't have the correct input
 wrong_adr = 0x122e

 # Flag is 10 characters
 flag = claripy.BVS("flag", 8 * 10)

 # Establish the entry state
 entry_state = target.factory.entry_state(stdin = flag)

 # Silence the warnings
 entry_state.options.add(angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY)

 # Flags consists only on numbers ('0' -> '9')
 for i in range(10):
     entry_state.solver.add(flag.get_byte(i) >= 48)
     entry_state.solver.add(flag.get_byte(i) <= 57)

 # Establish the simulation
 simulation = target.factory.simulation_manager(entry_state)

 # Start the simulation
 simulation.explore(find = desired_adr, avoid = wrong_adr)

 #code.interact(local=locals())

 solution = simulation.found[0].posix.dumps(0)

 print(solution)


```

### Conclusion
When running are python program we ran into errors because of how are computer python was
configure so some commands and functions in the angr library was not compatiable and able to
run. Our solution to this problem was to create a virtual enviroment that allowed us you use
the full extension of the angr library and get the password we wanted. We also utilized the
claripy library in which we use the claripy.bsv() function in order to create a bitvector that
would represent a symbolic vaiable of the flag. This was a useful tool for symbolic engines
like angr. This documentation shows the steps taken and thought process of how we exploited
a program in order to achieve our desired results.
