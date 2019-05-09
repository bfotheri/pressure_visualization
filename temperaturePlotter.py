import pyqtgraph as pg
import numpy as np
from random import random

class  CustomTempWidget(pg.GraphicsWindow):
    pg.setConfigOption('background', (20, 20, 20))
    pg.setConfigOption('foreground', 'w')
    time1 = 0
    def __init__(self, parent=None, sensor = None,**kargs):
        self.numTherms = 4
        self.data_size = 100
        pg.GraphicsWindow.__init__(self, **kargs)
        self.setParent(parent)
        self.setWindowTitle('pyqtgraph example: Scrolling Plots')
        self.thermistors = None
        labelStyle = {'color': '#FFF', 'font-size': '32px'}
        p = self.addPlot(labels =  {'left':'Temperature (°C)', 'bottom':'Time (s)'})
        # p1 = self.addPlot()
        p.setLabel('bottom', 'Time', 's', **labelStyle)
        p.setLabel('left', 'Temperature', '°C', **labelStyle)
        # self.data1 = np.zeros([self.data_size])
        # self.time = np.linspace(-20.,0.,200.)
        self.data = np.zeros([self.numTherms, 1])
        self.time = np.array([0])
        self.curve = []
        red = 255
        for idx in range(self.numTherms):
            val = [red, (255-red)//2, (255-red)]
            red -= 255 // self.numTherms
            # self.curve.append(p.plot(self.time[idx],self.data[idx], pen=pg.mkPen((255,167,0),width=5)))
            self.curve.append(p.plot(self.time,self.data[idx], pen=pg.mkPen(val,width=2)))
        p.setRange(yRange = (0,60))
        timer = pg.QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(200) # number of seconds (every 1000) for next update

    def update(self):
        # print(len(self.curve),self.curve[0])
        T = np.zeros([self.numTherms,1])
        if(self.thermistors is not None):
            if (len(self.data[0]) < self.data_size):
                for idx, thermistor in enumerate(self.thermistors):
                    T[idx] = np.array(thermistor.get_temperature())
                    # self.data[idx] = np.append(self.data[idx],T)
                    # self.curve[idx].setData(self.time, self.data)
                    self.curve[idx].setData(self.time, self.data[idx])
                self.time1 += 0.2
                self.time = np.append(self.time,self.time1)
                self.data = np.hstack((self.data,T))

            else:
                self.data[:,:-1] = self.data[:,1:]  # shift data in the array one sample left
                self.time[:-1] = self.time[1:]
                self.time1 += 0.2
                self.time[-1] = self.time1
                for idx in range(self.numTherms):

                    self.data[idx, -1] = self.thermistors[idx].get_temperature()
                    self.curve[idx].setData(self.time, self.data[idx])
        else:
            pass

    def passSensors(self, thermistors):
        self.thermistors = thermistors
if __name__ == '__main__':
    w = CustomWidget()
    w.show()
    QtGui.QApplication.instance().exec_()
