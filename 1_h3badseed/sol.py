from pwn import *

io = process('sh')

io.sendline('echo Hello, world')

io.recvline()
