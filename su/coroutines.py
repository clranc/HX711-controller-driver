import uasyncio as asyncio
import acf_network as a
import rfid as r

import network


class Coroutines:
    def __init__(self,db):
        self.db = db
        self.net = a.acf_network()
        self.rfid = r.RFID()

        self.isConnected = False

    async def testRoutine(self):
        while True:
            await asyncio.sleep(.1)
            print("I'm a test routine")

    async def testRoutine2(self):
        while True:
            await asyncio.sleep(.1)
            print("I'm also a test routine")

    async def networkRoutine(self):
        while True:
            await asyncio.sleep(.3)
            if self.net.wlan.status() == network.STAT_GOT_IP:
                self.isConnected = True
                print("connected")
                print( self.wlan.ifconfig() )
                
            else:
                self.isConnected() = False

    async def verifyConnection
