#!/usr/bin/env python
#
import urllib.request
from html.parser import HTMLParser
import html.entities

class ImageParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        if not hasattr(self, 'result'):
            self.result = []
        for name, value in attrs:
            if name == 'src':
                self.result.append(value)

def parseImage(data):
    parser = ImageParser()
    parser.feed(data)
    dataSet = set(x for x in parser.result)
    print ('\n'.join( sorted(dataSet) ))

def main():
    url = "http://www.google.co.kr"

    f = urllib.request.urlopen(url)
    charset = f.headers.get_content_charset()
    data = f.read().decode(charset)
    f.close()

    print (data)
    print ("\n>>>>>>>>> Fetch Images from", url)
    parseImage(data)

if __name__ == '__main__':
    main()
