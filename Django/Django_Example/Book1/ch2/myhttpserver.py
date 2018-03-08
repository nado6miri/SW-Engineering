#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        msg = "Hello World".encode('utf-8')
        
        self.wfile.write(msg)

if __name__ == '__main__':
    server = HTTPServer(('', 8888), MyHandler)
    print ("Started WebServer on port 8888...")
    print ("Press ^C to quit WebServer")
    server.serve_forever()
