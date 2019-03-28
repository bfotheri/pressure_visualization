import pyqtgraph as pg
import numpy as np

class  CustomWidget(pg.GraphicsWindow):
    pg.setConfigOption('background', (20, 20, 20))
    pg.setConfigOption('foreground', 'w')
    time1 = 0
    def __init__(self, parent=None, sensor = None,**kargs):
        self.data_size = 100
        pg.GraphicsWindow.__init__(self, **kargs)
        self.setParent(parent)
        self.setWindowTitle('pyqtgraph example: Scrolling Plots')
        self.p_sensor = None
        labelStyle = {'color': '#FFF', 'font-size': '32px'}
        p1 = self.addPlot(labels =  {'left':'Pressure (mmHg)', 'bottom':'Time (s)'})
        # p1 = self.addPlot()
        p1.setLabel('bottom', 'Time', 's', **labelStyle)
        p1.setLabel('left', 'Pressure', 'mmHg', **labelStyle)
        # self.data1 = np.zeros([self.data_size])
        # self.time = np.linspace(-20.,0.,200.)
        self.data1 = np.array([0])
        self.time = np.array([0])
        self.curve1 = p1.plot(self.time,self.data1, pen=pg.mkPen((0,167,255),width=5))
        p1.setRange(yRange= (0,300))
        timer = pg.QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(200) # number of seconds (every 1000) for next update

    def update(self):
        if (len(self.data1) < self.data_size):
            pressure = self.p_sensor.get_pressure()
            self.data1 = np.append(self.data1,pressure)
            self.time1 += 0.2
            self.time = np.append(self.time,self.time1)
            self.curve1.setData(self.time, self.data1)

        
        else:                    # (see also: np.roll)
            self.data1[:-1] = self.data1[1:]  # shift data in the array one sample left
            self.data1[-1] = self.p_sensor.get_pressure()
            # self.data1 = np.append(self.data1,self.p_sensor.get_pressure())
            self.time1 += 0.2
            self.time[:-1] = self.time[1:]
            self.time[-1] = self.time1
            # self.time = np.append(self.time,self.time1)
            # self.curve1.setData(self.data1[-100:])
            self.curve1.setData(self.time, self.data1)

    def passSensor(self,sensor):
        self.p_sensor = sensor
if __name__ == '__main__':
    w = CustomWidget()
    w.show()
    QtGui.QApplication.instance().exec_()
