#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import router
#import http.server
import json
import cgi

# HTTPRequestHandler class
class RequestHandler(BaseHTTPRequestHandler):

  # GET
  def do_GET(self):

        # Send headers
        self.send_header('Content-type','application/json')
        # Send response status code
        self.send_response(200)
        self.end_headers()

        response = json.dumps(router.routes[self.path])
        response += '\n'
        # Write content as utf-8 data
        self.wfile.write(response.encode())
        return

  def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        # add a property to the object
        message['received'] = 'ok'

        # Send headers
        self.send_header('Content-type','application/json')
        # Send response status code
        self.send_response(200)
        self.end_headers()

        # send the message back
        self.wfile.write((json.dumps(message)+'\n').encode())


def main() :
    print('starting server...')
    # Server settings
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, RequestHandler)
    print('running server...')
    httpd.serve_forever()

main()
