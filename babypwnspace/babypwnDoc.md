# Babypwn Challenge Solution Documnetation


## Steps

### 1. Create a Directory for Babypwn Files
We first created a directory for the babypwn files and we then relocated those files to that
directory.


### 2. Execute the file Command
We Ran the **file** command on the files within the directory to get the details such as there
names.  


### 3. Check File Security
We also use the **checksec** command to verify the security of the files, ensuring they are
secure.


### 4. Open and Examine Source Code
We opened a text editor and viewed the C file source code, upon examining the code we found
potential flaws. For instance, There was a character array with a maximum size of 32 bytes
yet there was an input statement that allowed for 64 bytes in which a user could input more
than the character array could contain causing a buffer overflow.


### 5. Understand Buffer Overflow
A buffer overflow occurs when when a software writes too much data into a buffer, causing the
excess data to overflow into nearby memory locations. This can cause issues like overwriting
a return address when a function is invoked.


### 6. Write Exploit Code
We created a program to exploit the identified vulnerabilities. Here is the code use:
```python
 
 from pwn import *
 
 # Start the process
 pw = process('babypwn')

 # Attach gdb debugger
 gdb.attach(pw, '''continue''')

 # Interact with the process
 pw.Interactive()

```
This code allows us to access the babypwn process and use the gdb debugger to observe what
happens when we input more characters than the array could hold.


### 7. Observe Segmentation Fault
After inputting an exceeded amount of characters, we observed a segmentation fault, indicating
that the code attempted to execute a program without permisson.


### 8. Capture the Flag
The segmentation fault helped in capturing the flag, we were able to successfully exploit this
challenge vulnerability.
 

## Results from the debugger

Program received signal SIGSEGV, Segmentation fault.
0x00000000004012c3 in main ()

[ Legend: Modified register | Code | Heap | Stack | String ]
---------------------------------------------------------------------------------------------
$rcx   : 0x0  
               
$rdx   : 0x0  
               
$rsp   : 0x00007fffffffddb8  →  0x0041414141414141 ("AAAAAAA"?)  

$rbp   : 0x4141414141414141 ("AAAAAAAA"?)  

$rsi   : 0x00007fffffffd7b0  →  ""This is the flag we win"\n"  

$rdi   : 0x00007fffffffd780  →  0x00007fffffffd7b0  →  ""This is the flag we win"\n"  

$rip   : 0x00000000004012c3  →  <main+00aa> ret  
 
$r15   : 0x0  
               
$eflags: [zero carry parity adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]  

$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00  
 
---------------------------------------------------------------------------------------------



## Conclusion
By following the above steps and using the provided code, we were able to exploit the buffer
overflow vulnerability and successfully complete the babypwn challenge.
