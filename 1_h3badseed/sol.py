from pwn import *
from ctypes import CDLL

libc = CDLL("libc.so.6")

libc.srand(libc.time(0))

final_time = libc.rand()

io = process('./time')

print(io.recvuntil(b'Enter your number: '))

io.sendline(b'%d' % final_time)

print(io.recvall())


