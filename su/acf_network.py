import network

def connectToParent():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    #temporary network for testing connections
    wlan.connect('klato','woof1984bear')
    while wlan.status() != network.STAT_GOT_IP:
        pass

    print("connected")
    print( wlan.ifconfig())

    return wlan
