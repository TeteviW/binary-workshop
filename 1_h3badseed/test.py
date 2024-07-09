#!/usr/bin/python3
from ctypes import CDLL

libc = CDLL("libc.so.6")

libc.srand(libc.time(0))

final_time = libc.rand()

print(final_time)

#this should generate a random sequence of number
