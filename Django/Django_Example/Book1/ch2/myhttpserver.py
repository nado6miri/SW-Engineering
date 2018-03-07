#!/usr/bin/env python

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.wfile.write("Hello World")

if __name__ == '__main__':
    server = HTTPServer(('', 8888), MyHandler)
    print "Started WebServer on port 8888..."
    print "Press ^C to quit WebServer"
    server.serve_forever()

