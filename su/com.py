import usocket as socket
import ujson

class FeederServ(object):
    def __init__(self, host, hostport, port):
        self.host = host
        self.hostport = hostport
        self.port = port
        self.hostServ  = socket.socket()
        self.serv = socket.socket()
        self.conn = None

    def waitConnection(self):
        self.serv.bind(('', self.port))
        self.serv.listen(5)
        self.conn = self.serv.accept()[0]
        print('Connected')

    def get(self):
        return (self.conn.readline())
