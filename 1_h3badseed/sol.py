from pwn import *

io = process('sh')

io.sendline(b'echo Hello, world')

thing = io.recvline()

print(thing)




