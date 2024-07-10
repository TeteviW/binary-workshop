from pwn import *

from ctypes import CDLL

# Loading the standard C library
libc = CDLL("libc.so.6")

# Seeding the random number generator with the current time
libc.srand(libc.time(0))

# Generating a random number using the seeded random number generator 
final_time = libc.rand()

# Starting a new process that runs the time program
io = process('./time')

# Receiving data from the process unil the string is encountered.
print(io.recvuntil(b'Enter your number: '))

# Sending the generated number converted to bytes to the process
io.sendline(b'%d' % final_time)

# Receiving all remaining data from the process and printing it.
print(io.recvall())


