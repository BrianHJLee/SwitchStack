from http.server import BaseHTTPRequestHandler, HTTPServer
#import ssl
import requests
import validators

hostName = "104.248.6.49"
serverPort = 80

def fileToBytes(path):
    in_file = open(path, "rb")
    data = in_file.read()
    in_file.close()
    return data

def isSubstack(url):
    return True

class SwitchServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if(self.path == "/"):
            self.serve_home()
            return
        
        url = self.path.replace("/", "", 1)

        if(not validators.url(url)):
            self.serve_404()
            return

        try:
            response = requests.get(url)
        except:
            self.serve_421()
            return

        if('x-cluster' not in response.headers or response.headers['x-cluster'] != 'substack'):
            self.serve_421()
            return

        if("Twitterbot" in self.headers):
            # TODO Return page with Twitter card
            self.serve_home()
            pass
        else:
            self.serve_redirect(url)
            pass
        
    def send_response(self, code, message=None):
        self.log_request(code)
        self.send_response_only(code, message)
        self.send_header('Date', self.date_time_string())

    #TODO clean these up into serve_file(self, status, file)
    def serve_404(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(fileToBytes("web/404.html"))
    
    def serve_421(self):
        self.send_response(421)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(fileToBytes("web/421.html"))

    def serve_home(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(fileToBytes("web/index.html"))
    
    def serve_redirect(self, loc):
        self.send_response(302)
        self.send_header("Location", loc)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(fileToBytes("web/302.html"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), SwitchServer)
    
    # HTTPS stuff
    '''
    webServer.socket = ssl.wrap_socket(
        webServer.socket,
        keyfile = "",
        certfile = "",
        server_side = True,
    )
    '''

    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
