#!/usr/bin/env python
#
import http.client
from urllib.parse import *
from urllib.request import *
#from urllib.parse import urlparse, urlunparse, urljoin, urlretrieve
from urllib import *
from html.parser import HTMLParser
import os

class ImageParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        if not hasattr(self, 'result'):
            self.result = []
        for name, value in attrs:
            if name == 'src':
                self.result.append(value)

def downloadImage(srcUrl, data):
    if not os.path.exists('DOWNLOAD') :
        os.makedirs('DOWNLOAD')

    parser = ImageParser()
    parser.feed(data)
    resultSet = set(x for x in parser.result)

    for x in sorted(resultSet) :
        src = urljoin(srcUrl, x)
        basename = os.path.basename(src)
        targetFile = os.path.join('DOWNLOAD', basename)

        print ("Downloading...", src)
        urlretrieve(src, targetFile)

def main():
    host = "www.google.co.kr"

    conn = http.client.HTTPConnection(host)
    conn.request("GET", '')
    resp = conn.getresponse()

    charset = resp.headers.get_content_charset()
    data = resp.read().decode(charset)
    conn.close()

    print ("\n>>>>>>>>> Download Images from", host)
    url = urlunparse(('http', host, '', '', '', ''))
    print(url)
    downloadImage(url, data)

if __name__ == '__main__':
    main()
