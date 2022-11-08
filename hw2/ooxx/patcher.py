def decrypt_string(txt:bytes)->bytes:
    res = b""
    for i in range(len(txt)):
        res += (txt[i] ^ 0x87).to_bytes(1, 'little', signed=True)
    return res
print(decrypt_string(b"\xdf\xa7\xd0\xee\xe9\xa6\x87"))
print(decrypt_string(b"\xc8\xa7\xd0\xee\xe9\xa6\x87"))
print(decrypt_string(b"\xd3\xee\xe2\xa6\x87"))

bins = bytearray(open("ooxx_f5c123f4e157e53d.exe", "rb").read())
bins[0xC72] = 0x85
open("ooxx_p.exe", "wb").write(bins)
flag = "FLAG{Y0u_Won_A_gaM3_yoU_cOuldn0T_pO5s16ly_w1n}"