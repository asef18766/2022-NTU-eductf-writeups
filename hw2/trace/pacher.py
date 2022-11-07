bins = bytearray(open("cs_2022_fall_ouo", "rb").read())
bad_bytes = bytearray(0xE8CBCCDEADBEEFE8.to_bytes(8, "little"))
while True:
    idx = bins.find(bad_bytes)
    if idx == -1:
        break
    bins[idx:idx+8] = [0x90] * 8
#open("cs_2022_fall_ouo.patched", "wb").write(bins)
flag = bytearray(bytes.fromhex("37 3D 30 36 0A 25 03 30 12 42 2E 3C 42 2E 40 37 2E 24 2E 12 30 3F 0C 00"))
for i in range(0x16+1):
    flag[i] ^= 0x71
print(bytes(flag))