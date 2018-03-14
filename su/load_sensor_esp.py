from machine import Pin
from array import array
import machine

# Need to double clock frequency because micropython is too slow
machine.freq(160000000)

dt = Pin(4, Pin.IN)
sck = Pin(5, Pin.OUT)

# Gram Conversion Value
scale = 743.0 

# Make sck is off
sck.off()
if sck.value() != 0:
    raise("Hardware malfunction sck pin5 is not changing value")

# Get 24 bit weight value
def getValue():
    # Initalize base reading value
    reading = 0x0

    # Check for available value
    while dt.value() != 0:
        pass

    # Shift in the 24 bit value
    for i in range(24):
        sck.value(1)
        sck.value(0)
        reading = (reading << 1) | dt.value()

    # 25th pulse for setting 128 gain
    sck.value(1)
    sck.value(0)
    
    # XOR to clear sign bit
    return reading ^ 0x800000

# Get an average of the weight readings
def getAvgValue(avg_cnt = 10):
    sum = 0
    cnt = avg_cnt
    while cnt > 0:
        sum += getValue()
        cnt -= 1

    return sum / avg_cnt

def getGram(avg_cnt = 10, offset = 0):
    weight = getAvgValue(avg_cnt) - offset
    return weight / scale
