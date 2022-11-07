bins = bytearray(open("ooxx_f5c123f4e157e53d.exe", "rb").read())
bins[0xC72] = 0x85
open("ooxx_p.exe", "wb").write(bins)
flag = "FLAG{Y0u_Won_A_gaM3_yoU_cOuldn0T_pO5s16ly_w1n}"