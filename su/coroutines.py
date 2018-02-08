import uasyncio as asyncio


async def testRoutine():
    while True:
        await asyncio.sleep(.1)
        print("I'm a test routine")


async def testRoutine2():
    while True:
        await asyncio.sleep(.1)
        print("I'm also a test routine")
