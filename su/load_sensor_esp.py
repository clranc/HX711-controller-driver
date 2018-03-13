from machine import Pin
import utime as ut

dt = Pin(4, Pin.IN)
sck = Pin(5, Pin.OUT)

# Gram Conversion Value
scale = 743.0 

# Making sure sck is off
sck.off()
if sck.value() != 0:
    raise ("Hardware malfunction sck pin5 is not changing value")

# Get 24 bit weight value
def getValue():
    # Initalize sck pulse count and base reading
    sck_cnt = 24
    reading = 0x0

    # Check for available valuemicropython wait
    while dt.value() != 0:
        pass

    # Shift in the 24 bit value
    while sck_cnt > 0:
        sck.on()
        #ut.sleep_us(1)
        sck.off()
        reading = (reading << 1)
        if (dt.value() == 1):
            reading += 1
        sck_cnt -= 1

    # reset pulse
    sck.on()
    sck.off()

    return reading #^ 0x800000

# Get an average of the weight readings
def getAvgValue(avg_cnt = 10):
    sum = 0
    cnt = avg_cnt
    while cnt > 0:
        sum += getValue()
        cnt -= 1

    return sum / avg_cnt

def getGram(avg_cnt = 10):
    weight = getAvgValue(avg_cnt)
    return weight / scale
