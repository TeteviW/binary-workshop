#!/usr/bin/env python3

from pwn import *

pw = process("babypwn")

gdb.attach(pw, '''
continue
'''
)

pw.interactive()
