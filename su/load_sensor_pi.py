import RPi.GPIO as rg

# Configuring GPIO pins
dt = 16
sck = 20
rg.setmode(rg.BCM)
rg.setup(dt, rg.IN)
rg.setup(sck, rg.OUT)

scale = 743.0

# Get 24 bit weight value
def getValue():
    # Initalize sck pulse count and base reading
    sck_cnt = 24
    reading = 0x0

    # Check for available valuemicropython wait
    while rg.input(dt) != 0:
        pass

    # Shift in the 24 bit value
    while sck_cnt > 0:
        rg.output(sck,1)
        rg.output(sck,0)
        reading = (reading << 1)
        if (rg.input(dt) == 1):
            reading += 1
        sck_cnt -= 1

    # reset pulse
    rg.output(sck,1)
    rg.output(sck,0)

    return reading ^ 0x800000

# Get an average of the weight readings
def getAvgValue(avg_cnt = 10):
    sum = 0
    cnt = avg_cnt
    while cnt > 0:
        sum += getValue()
        cnt -= 1

    return sum / avg_cnt

def getGram(avg_cnt = 10, offset=0):
    weight = getAvgValue(avg_cnt) - offset
    return weight / scale
