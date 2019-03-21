import time
# import board
# import busio
# import adafruit_ads1x15.ads1115 as ADS
# from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np

#TODO: Add some kind of error messaging for if the calibration points are done incorrectly
print('Pressure Sensor Module Imported')
class PressureSensor:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        self.chan = AnalogIn(ads, ADS.P0)
        #For the tuple, (x,y), x is the voltage at the pressure and y is the pressure
        self.high_point = (0,0) #TODO: Read these values in from a .txt file so we don't loose the calibration each time
        self.low_point = (0,0)
        self.slope = 1 #TODO: Make this zero again once we stop testing
        self.y_intercept = 0

    def set_high_point(self,pressure):
        voltage = np.random.randint(300)
        # voltage = self.chan.voltage #TODO: Read in and average multiple values to eliminate noise
        self.high_point = (voltage,pressure)
        self.calibrate()

    def set_low_point(self,pressure):
        # voltage = self.chan.voltage
        voltage = np.random.randint(300)
        self.low_point = (voltage,pressure)
        self.calibrate()

    def get_pressure(self):
        # voltage = self.chan.voltage
        voltage = np.random.randint(300)
        return self.slope*voltage + self.y_intercept

    def calibrate(self):
        self.slope = (self.high_point[1] - self.low_point[1]) / (self.high_point[0] - self.low_point[0]) #m = (y1 - y2) / (x1 - x2)
        self.y_intercept = self.low_point[1] - self.slope*self.low_point[0] #b = y - mx
