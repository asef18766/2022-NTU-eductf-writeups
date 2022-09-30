import os
from typing import List
import zipfile

def dirwalker(folder:str)->List[str]:
    res = []
    for f in os.listdir(folder):
        cur_path = f"{folder}/{f}"
        if os.path.isdir(cur_path):
            res += dirwalker(cur_path)
        else:
            res.append(cur_path)
    return res

if __name__ == "__main__":
    target_folders = [ i for i in os.listdir() if i.startswith("hw") ]
    while True:
        print("please select target folder:")
        for folder in target_folders:
            print(folder)
        target = input(">")
        if target not in target_folders:
            print(f"target {target} does not exsist")
        else:
            files = dirwalker(target)
            if f"{target}/writeup.pdf" not in files:
                raise FileNotFoundError("writeup.pdf does not exsist")
            files.remove(f"{target}/writeup.pdf")
            
            with zipfile.ZipFile("r11921a06.zip", "w") as zf:
                zf.write(f"{target}/writeup.pdf", "writeup.pdf")
                for f in files:
                    zf.write(f, "code/"+ f[len(target):])
            exit(0)