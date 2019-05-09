import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np

class PressureSensor:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c, address=0x48)
        self.chan = AnalogIn(ads, ADS.P0)
        #For the tuple, (x,y), x is the voltage at the pressure and y is the pressure
        self.range = 4.5
        self.high_point = [0,0]
        self.low_point = [0,0]
        self.slope = 0
        self.y_intercept = 0
        self.cal_file = '/home/pi/pressure_visualization/calibration.txt'
        # self.cal_file = '/home/brett/pressure_visualizer/calibration.txt'

        file = open(self.cal_file, 'r')
        for line in file:
            if (self.slope == 0):
                self.slope = float(line)
            else:
                self.y_intercept = float(line)
        print(self.slope,self.y_intercept)
        file.close()
    def set_high_point(self,pressure):
        #voltage = np.random.randint(self.range)
        voltage = self.chan.voltage #TODO: Read in and average multiple values to eliminate noise
        self.high_point = [voltage,pressure]
        self.calibrate()

    def set_low_point(self,pressure):
        voltage = self.chan.voltage
        #voltage = np.random.randint(self.range)
        self.low_point = [voltage,pressure]
        self.calibrate()

    def get_pressure(self):
        voltage = np.random.randint(self.range)
        # voltage = self.chan.voltage
        return self.slope*voltage + self.y_intercept

    def calibrate(self):
        self.slope = (self.high_point[1] - self.low_point[1]) / (self.high_point[0] - self.low_point[0]) #m = (y1 - y2) / (x1 - x2)
        self.y_intercept = self.low_point[1] - self.slope*self.low_point[0] #b = y - mx

        #Update the Calibration File
        file = open(self.cal_file, 'w')
        file.write(str(self.slope)+'\n')
        file.write(str(self.y_intercept))
        file.close()

class TemperatureSensor:
    def __init__(self,AnalogChannel=0):
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c, address=0x49)
        self.chan = AnalogIn(ads, ADS.P0)
        #For the tuple, (x,y), x is the voltage at the pressure and y is the pressure
        if AnalogChannel == 0:
                self.chan = AnalogIn(ads, ADS.P0)
        if AnalogChannel == 1:
                self.chan = AnalogIn(ads, ADS.P1)
   
        if AnalogChannel == 2:
                self.chan = AnalogIn(ads, ADS.P2)
        if AnalogChannel == 3:
                self.chan = AnalogIn(ads, ADS.P3)
        self.channel = AnalogChannel
        self.slope_idx = AnalogChannel*2 #This comes from how we how the temp_calibration.txt file is written and read from
        self.inter_idx = AnalogChannel*2 + 1
        self.range = 4.5
        self.high_point = [0,0]
        self.low_point = [0,0]
        self.slope = 0
        self.y_intercept = 0
        self.cal_file = '/home/pi/pressure_visualization/temperature_calibration.txt'
        # self.cal_file = '/home/brett/pressure_visualizer/temperature_calibration.txt'

        file = open(self.cal_file, 'r')
        for idx, line in enumerate(file):
            if (self.slope == 0 and idx == self.slope_idx):
                self.slope = float(line)
            elif(idx == self.inter_idx):
                self.y_intercept = float(line)
        print(self.slope,self.y_intercept)
        file.close()

    def set_high_point(self,temperature):
        # voltage = np.random.randint(self.range)
        voltage = self.chan.voltage #TODO: Read in and average multiple values to eliminate noise
        self.high_point = [voltage,temperature]
        self.calibrate()

    def set_low_point(self,temperature):
        voltage = self.chan.voltage
        # voltage = np.random.randint(self.range)
        self.low_point = [voltage,temperature]
        self.calibrate()

    def get_temperature(self):
        # voltage = np.random.randint(self.range)
        voltage = self.chan.voltage
        return self.slope*voltage + self.y_intercept

    def calibrate(self):
        self.slope = (self.high_point[1] - self.low_point[1]) / (self.high_point[0] - self.low_point[0]) #m = (y1 - y2) / (x1 - x2)
        self.y_intercept = self.low_point[1] - self.slope*self.low_point[0] #b = y - mx

        #Update the Calibration File
        if(self.channel == 0):
                file = open(self.cal_file, 'w')
        else:
                file = open(self.cal_file, 'a')
        file.write(str(self.slope)+'\n')
        file.write(str(self.y_intercept)+'\n')
        file.close()
