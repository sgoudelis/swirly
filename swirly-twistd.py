import cyclone.web
from twisted.application import internet
from twisted.application import service


class RequestHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        self.write("pipes")
        
        
webapp = cyclone.web.Application([
    (r"/payload", RequestHandler)
])

application = service.Application("swirly-twistd")
server = internet.TCPServer(8080, webapp, interface="0.0.0.0")
server.setServiceParent(application)
