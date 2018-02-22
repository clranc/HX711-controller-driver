import uasyncio as asyncio
import acf_network as a
#import rfid as r

import network


class Coroutines:
    def __init__(self,db):
        self.db = db
        self.net = a.acf_network(DEBUG=True)
        #self.rfid = r.RFID()
        self.key_verified = False

    async def networkRoutine(self):
        while True:
            await asyncio.sleep(.3)
            if self.net.isConnected() and self.key_verified == False:
                if self.net.verifyKey(self.db.getKey()) == False:
                    (b, key) = self.net.getNewKey()
                    if b == True:
                        self.key_verified = True
                        self.db.setKey(key)
                else:
                    self.key_verified = True

            elif self.net.isConnected() == False:
                self.key_verified = False




