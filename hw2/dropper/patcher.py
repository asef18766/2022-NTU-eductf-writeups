bins = bytearray(open("dropper_43741eb13c4a767e.bin", "rb").read())
# patch sleep
bins[0x2107:0x2107+4] = [0x90] * 4
open("dropper_p.bin", "wb").write(bins)