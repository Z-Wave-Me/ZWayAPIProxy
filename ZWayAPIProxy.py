#!/usr/bin/python3

import http.server
import socketserver
import socket
import requests
import sys
import os

REMOTE_SERVER = "http://localhost:8889"
PORT = 8888
HTDOCS = "htdocs"

class Server(http.server.SimpleHTTPRequestHandler):
    def prepareHeaders(self):
        headers = {}
        for h in ('Content-Type', 'Authentication Bearer', 'Cookie', 'ZWAYSession'):
            if h in self.headers:
                headers[h] = self.headers[h]
        
        headers['Authentication Bearer'] = '04203c9a1e7822c95270e74d04056b622c1ffef56c/315f9f9e-c53a-7efc-0312-8fe6084100af'
        headers['Authentication'] = 'Bearer: 04203c9a1e7822c95270e74d04056b622c1ffef56c/315f9f9e-c53a-7efc-0312-8fe6084100af'

        return headers
    
    def parseHeaders(self, r):
        self.send_response(r.status_code)
        for h in ('Content-Type', 'Authentication Bearer', 'Set-Cookie', 'ZWAYSession', 'Access-Control-Expose-Headers', 'Access-Control-Allow-Methods', 'Access-Control-Allow-Headers', 'Access-Control-Allow-Origin'):
            if h in r.headers:
                self.send_header(h, r.headers[h])
        self.end_headers()
    
    def isLocal(self):
        return not self.path.startswith("/ZAutomation") and not self.path.startswith("/ZWave.") and not self.path.startswith("/ZWaveAPI") and not self.path.startswith("/JS")
    
    def do_GET(self):
        if self.isLocal():
            return super().do_GET()
        
        r = requests.get(url = REMOTE_SERVER + self.path, headers = self.prepareHeaders())
        
        self.parseHeaders(r)
        
        self.wfile.write(r.content)
    
    
    def do_POST(self):
        if self.isLocal():
            return super().do_POST()
        
        r = requests.post(url = REMOTE_SERVER + self.path, headers = self.prepareHeaders(), data = self.rfile.read(int(self.headers['Content-Length'])))
        
        self.parseHeaders(r)
        self.wfile.write(r.content)
    
    def do_PUT(self):
        if self.isLocal():
            return super().do_PUT()
        
        r = requests.put(url = REMOTE_SERVER + self.path, headers = self.prepareHeaders(), data = self.rfile.read(int(self.headers['Content-Length'])))
        
        self.parseHeaders(r)
        self.wfile.write(r.content)
    
    
    def do_HEAD(self):
        if self.isLocal():
            return super().do_HEAD()

        r = requests.head(url = REMOTE_SERVER + self.path, headers = self.prepareHeaders())
        
        self.parseHeaders(r)
    
    def serve_forever(port, htdocs):
        os.chdir(htdocs)
        TCPServer(('', port), Server).serve_forever()

class TCPServer(socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        REMOTE_SERVER = sys.argv[1]
    
    if len(sys.argv) > 2:
        PORT = int(sys.argv[2])
    
    Server.serve_forever(PORT, HTDOCS)
