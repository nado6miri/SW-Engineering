#!/usr/bin/env python
#
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from urllib import *

url = "http://localhost:8888/cgi-bin/script.py"

data = {
    'language' : 'python',
    'framework' : 'django',
    'email' : 'kim@naver.com'
}

# UTF-8 형식으로 인코딩해버리면 bytes로 바뀝니다
encData = urlencode(data).encode('utf-8')
print(encData)

request = Request(url, encData)

response = urlopen(request)
print (response.read())
