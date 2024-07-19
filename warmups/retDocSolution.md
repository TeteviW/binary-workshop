# This is the Documentation of the ret2win ctf challenge


## Step-byStep Guide


This document outlines the steps taken to identify and exploit a buffer overflow vulnerability
using tools like Ghidra, _man_, _gdb-gef_, and Python. Each step is critical to understanding
the target system, identifying the vulnerability, and creating a succesful exploit.


### 1. Navigating Ghidra

**Description:**
Ghidra is a powerful open source reverse engineering tool that allows you to decompile and
analyze binary files.

* We first Launch Ghidra and created a new project

* We then import the target binary into the project

* We began to analyze the _main_ function, as it's typically the entry point of the program


### 2. Analyzing the Code and File

While navigating the binary in Ghidra our objective was to identify potential vulernabilities,
we were able to inspect function calls and examine the calls to other functions.

**Observations:**
* There was a function call to _read_ and we considered it a potential point of vulenrability,
espicially since it handled user input without proper bounds checking

* This is when we _file_ the ret2win32 file:
ret2win32: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked,
interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0,
BuildID[sha1]=e1596c11f85b3ed0881193fe40783e1da685b851, not stripped

* This is when we _checksec_ the ret2win32 file: 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      SymbolsFORTIFY Fortified       Fortifiable     FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   72 Symbols       No    0               3               ret2win32  


### 3. Understanding Function Behavior with man

**Description:**
The _man_ command in Linux provides a manuel for various functions, offering insights into
their behavior and potential vulnerabilities. After running the command on _read_, we were able
to understand how it works, including it's parameters and potential security implications.

**Key Points:**

* _read_ reads data from a file descriptor into a buffer

* It is crucial to ensure that the buffer is large enough to prevent overflow

* The code we examine did not provide a big enough buffer


### 4. Identifying the Target Memory Address

**Description:**
Finding the memory address you want to return to after exploiting the buffer overflow is
critical for hijacking.

* **Analyze the Binary:** Using Ghidra to identify the memory address you want to redirect
execution to.

* **Record the Address:** This address will be used later in the payload to overwrite the
return address. 

### 5. Finding the Buffer Offest using gdb-gef

**Description:**
_gdb-gef_ is a powerful extension for GDB that simplifies the process of debugging and exploit
development. We were able to use this tool to run the program and find the exact offset where
the buffer overflow occurs.


### 6. Writing the Exploit Code in Python
```python
 from pwn import * 

 # Sets information about the binary that affects how the pointer is defined
 context.bits = 32

 # initalizing the process
 pw = process("./ret2win32")

 # attach the gdb debugger to the process and set a break point at a certain memory address
 gdb.attach(pw, gdbscript = 'b *0x804862c')

 # Recieve data until the > symbol
 pw.recvuntil(b'>')

 # sends the right amount of A's to buffer overflow while also sending the address we want
 pw.sendline(b'A' * 44 + p64(0x804862c))

 # allows us to interact with the process
 pw.interactive()

```

### Conclusion
Following these steps provides a structered approach to identifying and exploiting buffer
overflow vulnerabilities. By leveraging tools like Ghidra, _man_, _gdb-gef_, and Python,
you can analyze the target binary, identify weaknesses, and create effective exploits. 
