import requests
files = {
    'file': ('main.py', open('main.py', 'rb')),
}
with requests.post("https://pyscript.ctf.zoolab.org/", files=files) as resp:
    print(resp.text)