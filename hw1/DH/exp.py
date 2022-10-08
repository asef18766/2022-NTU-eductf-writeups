#! /usr/bin/python3
from pwn import remote
from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes, inverse
import random

proc = remote("edu-ctf.zoolab.org", 10104)
p = int(proc.recvline().strip())
if (p - 1) % 3 != 0:
    raise Exception("pls retry")
def find_gen():
    while True:
        gen = random.randint(2, p - 2)
        if pow(gen, (p-1)//3, p) != 1:
            return gen
g = pow(find_gen(), (p-1)//3, p)
print(f"gen: {g}")
gen = pow(g, (p-1)//3, p)
proc.sendline(str(gen).encode())
c = proc.recvline()
if c == b'Bad :(\n':
    raise Exception("pls retry")
c = int(c)
print(c)
for i in range(3):
    print(long_to_bytes(c * inverse(pow(gen, i, p), p) % p))