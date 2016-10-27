import os
import socket
import fcntl
import struct
import urllib
import SocketServer
import BaseHTTPServer
from multiprocessing import Process
from datetime import datetime, date
from urlparse import urlparse

global PORT
global SERVER_URL

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

  # '192.168.0.110'


def getLogTime():
    return date.today().strftime('%Y-%m-%d ') + datetime.now().strftime('%H:%M:%S.%f ')[:-3] + ' ' + get_ip_address('eth0') + ":" + str(PORT) + ' '

def process():
    print(getLogTime() + "Detached Processing from  " )
    resp = urllib.urlopen(SERVER_URL)
    if (resp.getcode() != 200) :
        print(getLogTime() + "Status:" + str(resp.getcode()) + ", Body:" + str(resp.read()))
        print(getLogTime() + SERVER_URL + "is not accessible")
    else :
        print(getLogTime() + "Status:" + str(resp.getcode()) + ", Body:" + str(resp.read()))
        print(getLogTime() + "HTTP GET Req reach to " + SERVER_URL)


class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        #Get Download URL & Report Callback URL
        # params = urlparse(self.path).query
        elem = urlparse(self.path).path.split('/')
        print elem
        print self.address_string()

        if len(elem) > 2:
            self.respond("Unknow request", 400)

        # HTTP status processing /status
        elif elem[1].lower() == "status" :
            self.respond("Service OK")

        # HTTP request processing /eco
        elif elem[1].lower() == "eco" :
            self.respond("Request received")

        # HTTP request processing /forward
        elif elem[1].lower() == "forward" :
            #p = Process(target=process, args=())
            #p.start()
            resp = urllib.urlopen(SERVER_URL)
            if (resp.getcode() != 200) :
                print(getLogTime() + "Status:" + str(resp.getcode()) + ", Body:" + str(resp.read()))
                print(getLogTime() + SERVER_URL + "is not accessible")
                self.respond(SERVER_URL + "is not accessible", 400)
            else :
                print(getLogTime() + "Status:" + str(resp.getcode()) + ", Body:" + str(resp.read()))
                print(getLogTime() + "HTTP GET Req reach to " + SERVER_URL)
                self.respond("HTTP GET Req reach to " + SERVER_URL)

        else :
            self.respond("Unknow request", 400)

        #query_components = dict(qc.split("=") for qc in params.split("&"))
        #print(getLogTime() + "Receive Params URL:" + str(query_components["url"]) +\
        #                     "AssetId : " + str(query_components["assetId"]))
        #print(getLogTime() + "Receiving : " + self.requestline)
        #p = Process(target=process, args=(query_components["url"],
        #                                  query_components["assetId"],
        #                                  (lambda x : "videoonly" in x and x["videoonly"] or "0")(query_components),
        #                                  query_components["callback_success"],
        #                                  query_components["callback_error"], ))
        #p.start()


    def do_POST(self):
        self.do_GET() # currently same as post, but can be anything


    def respond(self, response, status=200):
        self.send_response(status, response)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response)


if __name__=='__main__':

    #config = ConfigParser.ConfigParser()
    #config.read('cdnAgent.conf')

    PORT = os.getenv('self.port', 8001)
    print PORT
    SERVER_URL="http://"+os.getenv('server.ip', "127.0.0.1") + ":" + str(os.getenv('server.port', 8001)) + "/eco"
    print SERVER_URL
    httpd = SocketServer.TCPServer(("", int(PORT)), MyRequestHandler)
    print(getLogTime() + "service1 at port " + str(PORT))
    try:
        httpd.serve_forever()
    except:
        httpd.server_close()

