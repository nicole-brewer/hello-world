#!/usr/bin/python3

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket

# The BaseHTTPRequestHandler class is used to handle the HTTP requests that arrive at the server.
# Here we extend this class and make a custom response to a GET request
class myRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # send status code 200 OK
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # send html message
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        message = 'Hello client! Your address is ' + self.client_address[0] + ' on port ' + str(self.client_address[1]) + '.\n'
        message = message +  'You\'ve hit ' + hostname + '. server_name: ' + self.server.server_name + '. Port ' + str(self.server.server_port) + '. Server IP: ' + ip + '.'
        self.wfile.write(message)
        return

print("Kubia server starting... Press ^C to shut down.")
try: 
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, myRequestHandler)
    httpd.serve_forever()    
except KeyboardInterrupt:
    print('^C received: shutting down web server')
    httpd.socket.close()   # localhost, port 8080


