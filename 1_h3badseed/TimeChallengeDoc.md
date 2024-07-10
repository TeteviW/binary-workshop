# Creating a random number generator that matches a random sequence

This documenet provides the process on how we exploited a seed that
genarates a number sequence in order to solve a challenge that requires
you to guess the right randomly generated number.


## Theses are the steps taken to develop a solution:

**step 1:** We first look at the main function in ghidra and we see that they are using a rand()
function from a C library that generates a random number sequence using the current time as the
seed. Knowing this we figure out that if we can get the same seed that they are using we can get
the same number sequence generated.  


**step 2:** We then start coding a python program in order to generate the same number, however
because we are writing in python there is no guarantees that that the Python program we are 
writing will produce the same result since the original code uses a C function. Therefore we 
decided to wrap a C library that translates Python calls into C calls and vice versa allowing
Python code to use the functionality provided by the C library. The library we used is called
Ctypes a foreign function in Python that allows calling functions in DLLs or shared library.  


**step 3:** We wrote the python code using the Ctype library that uses the current time as the
seed and pwntools library to interact with the process. 

```python
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

```
In this code we utilize the pwntools to interact with a shell process that expects a number
input that was generated predictably in which we were able to exploit this vulnerability. 
