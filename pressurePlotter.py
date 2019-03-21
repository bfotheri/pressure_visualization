import pyqtgraph as pg
import numpy as np

class  CustomWidget(pg.GraphicsWindow):
    pg.setConfigOption('background', (20, 20, 20))
    pg.setConfigOption('foreground', 'w')
    ptr1 = 0
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
        self.data1 = np.array([])
        # self.curve1 = p1.plot(self.data1, pen=(1,3))
        self.curve1 = p1.plot(self.data1, pen=(0,167,255))
        p1.setRange(yRange= (0,30))
        timer = pg.QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(200) # number of seconds (every 1000) for next update

    def update(self):
        if (len(self.data1) < self.data_size):
            pressure = self.p_sensor.get_pressure()
            self.data1 = np.append(self.data1,pressure)
            self.ptr1 += 0.2
            self.curve1.setData(self.data1)
            self.curve1.setPos(self.ptr1, 0)
        else:
            self.data1[:-1] = self.data1[1:]  # shift data in the array one sample left
                                # (see also: np.roll)
            self.data1[-1] = self.p_sensor.get_pressure()
            self.ptr1 += 0.2
            self.curve1.setData(self.data1)
            self.curve1.setPos(self.ptr1, 0)
    def passSensor(self,sensor):
        self.p_sensor = sensor
if __name__ == '__main__':
    w = CustomWidget()
    w.show()
    QtGui.QApplication.instance().exec_()
