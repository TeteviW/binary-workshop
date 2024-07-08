from pwn import *

io = process('./time')

print(io.recvuntil(b'Enter your number: '))

io.sendline(b'9090')

print(io.recvline())

print(io.recvline())

print(io.recvline())


