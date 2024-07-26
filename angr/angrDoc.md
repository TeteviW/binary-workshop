# This is the documentation of the angr ctf challenge for r100

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

* This is when we _file_ the r100 file:
r100: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter
/lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24,
BuildID[sha1]=0f464824cc8ee321ef9a80a799c70b1b6aec8168, stripped

* This is when we _checksec_ the r100 file:
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      SymbolsFORTIFY Fortified       Fortifiable     FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols       No    0               2               r100                                  



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

 # Establish the Angr Project
 target = angr.Project('r100')

 # Specify the desired address which means we have the correct input
 desired_adr = 0x400849

 # Specify the address which if it executes means we don't have the correct input
 wrong_adr = 0x40085a

 # Establish the entry state
 entry_state = target.factory.entry_state(args=["./fairlight"])

 # Establish the simulation
 simulation = target.factory.simulation_manager(entry_state)

 # Start the simulation
 simulation.explore(find = desired_adr, avoid = wrong_adr)

 solution = simulation.found[0].posix.dumps(0)
 print(solution)

```

### Conclusion
When running are python program we ran into errors because of how are computer python was
configure so some commands and functions in the angr library was not compatiable and able to
run. Our solution to this problem was to create a virtual enviroment that allowed us you use
the full extension of the angr library and get the password we wanted. This documentation
shows the steps taken and thought process of how we exploited a program in order to achieve
our desired results.
