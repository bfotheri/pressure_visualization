from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_MainWindow import Ui_MainWindow
import numpy as np

class MainUi(Ui_MainWindow):
    def __init__(self,pressureSensor):
        #Flags and Properties
        self.calibrateClicked = True
        self.toggleStatus = 'graph'
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updatePressure)
        self.timer.start(200) # number of milliseconds (every 200) for next update
        self.counter = 0
        self.disp_res = 5 #Display resolution of 5 mmHg
        self.sensor = pressureSensor


    def toggleVisuals(self):
        if(self.toggleStatus == 'graph'):
            self.toggleButton.setText("Number")
            self.widget.hide()
            self.pressureValue.show()
            self.pressureUnitsLabel.show()
            self.toggleStatus = 'number'
        elif(self.toggleStatus == 'number'):
            self.toggleButton.setText("Graph")
            self.widget.show()
            self.pressureValue.hide()
            self.pressureUnitsLabel.hide()
            self.toggleStatus = 'graph'

    def updatePressure(self):
        pressure = self.sensor.get_pressure()
        extra = (pressure % self.disp_res)
        disp_pressure = pressure - extra + round(float(extra)/self.disp_res)*self.disp_res
        self.pressureValue.setText(str(int(disp_pressure)))

    def showCalibrationButtons(self):
          if(self.calibrateClicked):
              self.upperCalButton.hide()
              self.upperCalField.hide()
              self.upperCalLabel.hide()
              self.lowerCalButton.hide()
              self.lowerCalField.hide()
              self.lowerCalLabel.hide()
              self.calibrateClicked = False
          else:
              self.upperCalButton.show()
              self.upperCalField.show()
              self.upperCalLabel.show()
              self.lowerCalButton.show()
              self.lowerCalField.show()
              self.lowerCalLabel.show()
              self.calibrateClicked = True

    def setUpperPoint(self):
        pressure = int(self.upperCalField.toPlainText())
        self.sensor.set_high_point(pressure)

    def setLowerPoint(self):
        pressure = int(self.lowerCalField.toPlainText())
        self.sensor.set_low_point(pressure)

    def setupSignals(self):
        #Hide the pressure Value initially
        self.pressureValue.hide()
        self.pressureUnitsLabel.hide()

        self.widget.passSensor(self.sensor)

        #Signals
        self.showCalibrationButtons()
        self.calibrateButton.clicked.connect(lambda:self.showCalibrationButtons())
        self.toggleButton.clicked.connect(lambda:self.toggleVisuals())
        self.upperCalButton.clicked.connect(lambda:self.setUpperPoint())
        self.lowerCalButton.clicked.connect(lambda:self.setLowerPoint())
