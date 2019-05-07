from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_MainWindow import Ui_MainWindow
import numpy as np
import csv

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
        font = QtGui.QFont()
        self.font = font
        self.record = False
        self.file = open('logging_file.csv', mode='w')
        self.csv_writer = csv.writer(self.file)

    def toggleVisuals(self):
        if(self.toggleStatus == 'graph'):
            self.font.setPointSize(36)
            self.toggleButton.setFont(self.font)
            self.toggleButton.setText("Graph")
            self.widget.hide()
            self.pressureValue.show()
            self.pressureUnitsLabel.show()
            self.toggleStatus = 'number'
        elif(self.toggleStatus == 'number'):
            self.font.setPointSize(32)
            self.toggleButton.setFont(self.font)
            self.toggleButton.setText("Number")
            self.widget.show()
            self.pressureValue.hide()
            self.pressureUnitsLabel.hide()
            self.toggleStatus = 'graph'

    def updatePressure(self):
        pressure = self.sensor.get_pressure()
        extra = (pressure % self.disp_res)
        disp_pressure = pressure - extra + round(float(extra)/self.disp_res)*self.disp_res
        self.pressureValue.setText(str(int(disp_pressure)))
        if self.record == True:
            pressure = int(pressure)
            #self.csv_writer.writerows([[pressure, pressure, pressure],[pressure, pressure, pressure]])
            #print(pressure)
        else:
            pass

    def showCalibrationButtons(self):
          if(self.calibrateClicked):
              self.font.setPointSize(30)
              self.calibrateButton.setFont(self.font)
              self.calibrateButton.setText("Calibrate")
              self.calibrateButton.setGeometry(QtCore.QRect(490, 20, 211, 81))
              self.calibrateButton.setStyleSheet("background-color: rgb(0,167,255);")
              self.logButton.show()
              self.upperCalButton.hide()
              self.upperCalField.hide()
              self.upperCalLabel.hide()
              self.lowerCalButton.hide()
              self.lowerCalField.hide()
              self.lowerCalLabel.hide()
              self.calibrateClicked = False
          else:
              self.font.setPointSize(36)
              self.calibrateButton.setFont(self.font)
              self.calibrateButton.setText("Hide")
              self.calibrateButton.setGeometry(QtCore.QRect(350, 20, 211, 81))
              self.calibrateButton.setStyleSheet("background-color: rgb(0, 103, 147);")
              self.logButton.hide()
              self.upperCalButton.show()
              self.upperCalField.show()
              self.upperCalLabel.show()
              self.lowerCalButton.show()
              self.lowerCalField.show()
              self.lowerCalLabel.show()
              self.calibrateClicked = True

    def startLogging(self):
        if not self.record:
            self.record = True
            self.logButton.setText("Stop")
            self.logButton.setStyleSheet("background-color: rgb(255,10,10);")
        else:
            self.record = False
            self.logButton.setText("Record")
            self.logButton.setStyleSheet("background-color: rgb(0,167, 255);")

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
        self.logButton.clicked.connect(lambda:self.startLogging())
