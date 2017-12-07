import network

def connectToPhone():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('klato','woof1984bear')
    print(wlan.ifconfig())
    return wlan
