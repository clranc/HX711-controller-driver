import usocket as socket
import ujson
import ure
import urequests

class FeederServ(object):
    def __init__(self, port):
        self.port = port
        self.serv = socket.socket()
        self.serv.bind(('', self.port))
        self.serv.listen(5)

    def waitConnection(self):
        size = 1024
        re = ure.compile('\r\n')
        conn, addr= self.serv.accept()
        while True:
            print('Connected')
            msg = conn.recv(size)
            print(re.split(msg))
            conn.send(b'Recieved')

def http_respons(response_status, content_type, content_length):
        http_response = ("HTTP/1.1" + response_status + "\r\n" + \
                         "Server: python-custom\r\n" +\
                         "Content-Length: " + str(content_length) + "\r\n" + \
                         "Content-Type: " + content_type + "\r\n" + \
                         "Connection: Closed\r\n" )
