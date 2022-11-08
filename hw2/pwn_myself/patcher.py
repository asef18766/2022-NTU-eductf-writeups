bins = bytearray(open("pwn_myself", "rb").read())
# comparison
bins[0x00664A2] = 0x74
# decrypt item (lea pc relative address)
rip = 0x0664BE
dst = 0x0397040
bins[0x00664BA:0x00664BA+4] = (dst - rip).to_bytes(4, 'little')
# decrypt len
bins[0x00664B3] = 0x30

open("pwn_myself.patched", "wb").write(bins)