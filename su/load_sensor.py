import os
if os.__name__ == 'uos':
    import load_sensor_esp as loadsensor
else : 
    import load_sensor_pi as loadsensor

class LoadSensor:
    def __init__(self, calib = 100):
        self.getValue = loadsensor.getValue
        self.getAvgValue = loadsensor.getAvgValue
        self.__getGram = loadsensor.getGram
        self.__offset = self.getAvgValue(calib)
    def getGram(self, avg_cnt=10):
        return self.__getGram(avg_cnt, self.__offset)
    def calibrate(self, avg_cnt = 20):
        self.__offset = self.getAvgValue(avg_cnt)
