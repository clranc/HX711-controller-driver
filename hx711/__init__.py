import os
if os.__name__ == 'uos':
    from .hx711_esp_pin import DTPin, SCKPin, hx711_init
    DTP=4
    SCKP=5
else :
    from .hx711_pi_pin import DTPin, SCKPin, hx711_init
    DTP=35
    SCKP=37

INITMODE=True

from array import array

# Gram Conversion Value
scale = 743.0
# reading buffer size
buffer_size = 10
valid_buf_cnt = 7
readtolerance = 100

# Jam Checking Values
jam_check_cnt = 5
FULL = 0
FEEDING = 1
JAMMED = 2

# caliCheck :: int -> bool
caliCheck = lambda x: abst(x,readtolerance)
# fullCheck :: int -> (int -> bool)
fullCheck = lambda t: lambda x: gte(x,t*scale)
# ltt :: int -> int -> bool
gte = lambda x,t: x >= t
# absdt :: int -> int -> int -> bool
absdt = lambda x1,x2,t: abs(x1 - x2) < t
# abst :: int -> int -> bool
abst = lambda x,t: abs(x) < t

class LoadSensor:
    def __init__(self,dtp=DTP,sckp=SCKP,initmode=INITMODE):
        hx711_init(initmode)
        self.dt = DTPin(dtp)
        self.sck = SCKPin(sckp)
        self.buf = array('q',[0]*buffer_size)
        self.bufi = 0
        self.bufload = True
        self.jamcnt = 0

        # Make sure sck is off
        self.sck.off()
        if self.sck.value() != 0:
            raise("Hardware malfunction sck is not changing value")
        self.__offset = 0
        self.calibrate()

    def __buf_add__(self):
        self.buf[self.bufi] = self.getValue() - self.__offset
        if self.bufi < buffer_size - 1:
            self.bufi += 1
        else:
            self.bufi = 0

    def __buf_check__(self, lf):
        cnt = 0
        for val in self.buf:
            if lf(val):
                cnt += 1
        return cnt >= valid_buf_cnt

    def __buf_load__(self):
        for i in range(buffer_size):
            self.__buf_add__()

    def __load_avg__(self):
        cnt = 0
        sum = 0
        for i in range(buffer_size):
            difl = abs(self.buf[i-1] - self.buf[i])
            difr = abs(self.buf[i-1] - self.buf[i-2])
            if difl < readtolerance and difr < readtolerance:
                cnt += 1
                sum += self.buf[i-1]
        if cnt >= valid_buf_cnt:
            return sum/cnt
        return None

    def __is_jammed__(self):
        cnt = 0
        for i in range(buffer_size):
            difl = abs(self.buf[i-1] - self.buf[i])
            difr = abs(self.buf[i-1] - self.buf[i-2])
            if difl > readtolerance or difr > readtolerance:
                cnt += 1
        return cnt > buffer_size - valid_buf_cnt

    # Get 24 bit weight value
    def getValue(self):
        # Initalize base reading value
        reading = 0x0

        # Check for available value
        while self.dt.value() != 0:
            pass

        # Shift in the 24 bit value
        for i in range(24):
            self.sck.pulse()
            reading = (reading << 1) | self.dt.value()

        # 25th pulse for setting 128 gain
        self.sck.pulse()

        # XOR to clear sign bit
        return reading ^ 0x800000

    # Get an average of the weight readings
    def getAvgValue(self, avg_cnt = 10):
        sum = 0
        cnt = avg_cnt
        while cnt > 0:
            sum += self.getValue()
            cnt -= 1
        return sum / avg_cnt

    def gramToLoadVal(self, weight):
        return int(weight*scale)

    def getGram_cur(self):
        avg = self.__load_avg__()
        if avg != None:
            avg = avg/scale
        return avg

    def getGram(self):
        self.__buf_load__()
        while 1:
            avg = self.__load_avg__()
            if avg == None:
                self.__buf_add__()
            else:
                break
        return avg/scale

    def isLoadValid(self, lf):
        if self.bufload:
            self.__buf_load__()
        else:
            self.__buf_add__()
        self.bufload = self.__buf_check__(lf)
        return self.bufload

    def loadState(self, feed):
        valid = self.isLoadValid(fullCheck(feed))
        if self.jamcnt == jam_check_cnt:
            self.jamcnt = 0
            jam = self.__is_jammed__()
        else:
            self.jamcnt += 1
            jam = False

        if (valid):
            return FULL
        elif(jam):
            return JAMMED
        else:
            return FEEDING

    def calibrate(self,avg_cnt=5):
        self.__offset = int(self.getAvgValue(avg_cnt))
        # Checks to see if 70% of the buffer values are within the
        # tolerable offset of 100 before gram conversion. Most values
        # seem to fall within this tolerance which equates to about a
        # .13 Gram offset from the 0 reading
        while self.isLoadValid(caliCheck) == False:
            self.__offset = int(self.getAvgValue(avg_cnt))
