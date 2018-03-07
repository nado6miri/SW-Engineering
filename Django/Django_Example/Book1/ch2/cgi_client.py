#!/usr/bin/env python
#
import urllib2
from urllib import urlencode

url = "http://localhost:8888/cgi-bin/script.py"
data = {
    'language' : 'python',
    'framework' : 'django',
    'email' : 'kim@naver.com'
}
encData = urlencode(data)

f = urllib2.urlopen(url, encData)	# POST
print f.read()
