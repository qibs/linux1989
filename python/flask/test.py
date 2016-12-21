import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
'''#SimpleHTTPRequestHandler.path=r"e:\"
HandlerClass = SimpleHTTPRequestHandler
ServerClass = BaseHTTPServer.HTTPServer
Protocol = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('127.0.0.1', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
class TestHTTPHandle(BaseHTTPRequestHandler):
    def do_GET(self):
        buf = 'It works'
        self.protocal_version = 'HTTP / 1.1'

        self.send_response(200)

        self.send_header("Welcome", "Contect")

        self.end_headers()

        self.wfile.write(buf)


def start_server(port):
    http_server = HTTPServer(('', int(port)),TestHTTPHandle)
    http_server.serve_forever()
start_server(2000)'''''
#aa="this is a gird"
#print aa.split()
def a(n):
    for i in range(n):
        yield i,1
for i in a(9):
    key,value=i
    print value