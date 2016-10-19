import SocketServer
import BaseHTTPServer
from datetime import datetime, date
from urlparse import urlparse

def getLogTime():
    return date.today().strftime('%Y-%m-%d ') + datetime.now().strftime('%H:%M:%S.%f ')[:-3] + ' '

def process():
    print(getLogTime() + "Detached Processing  > ")

class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        #Get Download URL & Report Callback URL
        params = urlparse(self.path).query

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

        #Reply 200 to Client
        response = ("Request received");
        self.respond(response)

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

    #PORT = config.get('SETTINGS', 'SERVICE_PORT')
    PORT = 8001
    httpd = SocketServer.TCPServer(("", int(PORT)), MyRequestHandler)
    print(getLogTime() + "service1 at port " + str(PORT))
    httpd.serve_forever()

