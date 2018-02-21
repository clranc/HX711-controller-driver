import urequests as r
import machine
import network

newkey_key = "CanIHasCheezburger"

class acf_network:
    def __init__(self,DEBUG=False):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(true())
        self.connect()
        self.DEBUG = DEBUG
        self.connected = False

    def connect(self):
        self.wlan.connect('TestKitters','FeedUrKatz')

    def isConnected(self):
        if self.wlan.status() == network.STAT_GOT_IP and self.connected == False:
            self.connected = True
            if self.DEBUG == True:
                print("connected")
                print( self.wlan.ifconfig() )
        elif self.wlan.status() != network.STAT_GOT_IP:
            self.connected = False
            if self.DEBUG == True:
                print("connection status : %d", self.wlan.status())
        return self.connected

    # Checks to see if the stored key is valid with the pi server
    def verifyKey(self, key):
        resp = r.get('http://'+self.wlan.ifconfig()[2]+":8080",json = {'key':key})
        b = resp.json()['bool']
        if b == 'T':
            return True
        else:
            return False

    def getKey(self):
        resp = r.post('http://'+self.wlan.ifconfig()[2]+":8080", json = {'id':machine.unique_id(), 'key': newkey_key})
        b = resp.json()['bool']
        key = resp.json()['key']
        if b == 'T':
            b = True
        else :
            b = False
        return (b, key)

