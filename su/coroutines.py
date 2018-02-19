import uasyncio as asyncio

class Coroutines:
    def __init__(self,db):
        self.db = db

    async def testRoutine(self):
        while True:
            await asyncio.sleep(.1)
            print("I'm a test routine")
    
    
    async def testRoutine2(self):
        while True:
            await asyncio.sleep(.1)
            print("I'm also a test routine")
