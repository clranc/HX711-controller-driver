import os
if os.__name__ == 'uos':
    import load_sensor_esp as loadsensor
else : 
    import load_sensor_pi as loadsensor

class LoadSensor:
    def __init__(self):
        self.getValue = loadsensor.getValue
        self.getAvgValue = loadsensor.getAvgValue
        self.getGram = loadsensor.getGram
