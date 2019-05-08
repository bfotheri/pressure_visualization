from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_MainWindow import Ui_MainWindow
import numpy as np
import csv

class MainUi(Ui_MainWindow):
    def __init__(self,pressureSensor, temperatureSensors):
        #Flags and Properties
        self.calibrateClicked = True
        self.numGraphToggleStatus = 'graph'
        self.pressTempToggleStatus = 'pressure'
        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.updatePressure)
        self.timer1.start(200) # number of milliseconds (every 200) for next update
        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(self.updateTemperature)
        self.timer2.start(200) # number of milliseconds (every 200) for next update
        self.counter = 0
        self.disp_res = 5 #Display resolution of 5 mmHg
        self.pressure_sensor = pressureSensor
        self.temperature_sensors = temperatureSensors
        font = QtGui.QFont()
        self.font = font
        self.record = False
        self.file = open('logging_file.csv', mode='w')
        self.csv_writer = csv.writer(self.file)

    def toggleVisuals(self, secondary = False):
        # Secondary means we're using this function for the temp/pressure button and
        # not for the graph/number, so we need to change the logic up a bit
        self.hideVisuals()
        if(secondary):
            if(self.numGraphToggleStatus == 'graph'):
                self.numGraphToggleStatus = 'number'
            else:
                self.numGraphToggleStatus = 'graph'
        if(self.numGraphToggleStatus == 'graph'):
            self.font.setPointSize(36)
            self.numGraphToggleButton.setFont(self.font)
            self.numGraphToggleButton.setText("Graph")
            self.numGraphToggleStatus = 'number'

            if(self.pressTempToggleStatus == 'pressure'):
                self.pressureValue.show()
                self.pressureUnitsLabel.show()
            elif(self.pressTempToggleStatus == 'temperature'):
                self.showTempBoxes()
                self.temperatureUnitsLabel.show()

        elif(self.numGraphToggleStatus == 'number'):
            self.font.setPointSize(32)
            self.numGraphToggleButton.setFont(self.font)
            self.numGraphToggleButton.setText("Number")
            self.numGraphToggleStatus = 'graph'

            if(self.pressTempToggleStatus == 'pressure'):
                self.pressureGraph.show()
            elif(self.pressTempToggleStatus == 'temperature'):
                self.temperatureGraph.show()

    def hideVisuals(self):
        self.temperatureGraph.hide()
        self.pressureGraph.hide()
        self.pressureValue.hide()
        self.pressureUnitsLabel.hide()
        self.temperatureUnitsLabel.hide()
        self.hideTempBoxes()

    def updatePressure(self):
        pressure = self.pressure_sensor.get_pressure()
        extra = (pressure % self.disp_res)
        disp_pressure = pressure - extra + round(float(extra)/self.disp_res)*self.disp_res
        self.pressureValue.setText(str(int(disp_pressure)))
        if self.record == True:
            pressure = int(pressure)
            #self.csv_writer.writerows([[pressure, pressure, pressure],[pressure, pressure, pressure]])
            #print(pressure)
        else:
            pass

    def updateTemperature(self):
        temp = self.pressure_sensor.get_pressure()
        extra = (temp % self.disp_res)
        disp_pressure = temp - extra + round(float(extra)/self.disp_res)*self.disp_res
        self.temperatureValue0.setText(str(int(disp_pressure)))
        self.temperatureValue1.setText(str(int(disp_pressure)))
        self.temperatureValue2.setText(str(int(disp_pressure)))
        self.temperatureValue3.setText(str(int(disp_pressure)))
        if self.record == True:
            pass
            # temp = int(temp)
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
        self.pressure_sensor.set_high_point(pressure)

    def setLowerPoint(self):
        pressure = int(self.lowerCalField.toPlainText())
        self.pressure_sensor.set_low_point(pressure)

    def toggleTempPress(self):
        if(self.pressTempToggleStatus == 'pressure'):
            self.pressTempToggleButton.setText("Pressure")
            self.pressTempToggleButton.setStyleSheet("background-color: rgb(0,167, 255);")
            self.pressTempToggleStatus = 'temperature'

            self.GUI_Title.setText('Temperature Monitor')
            # if(self.)
        elif(self.pressTempToggleStatus == 'temperature'):
            self.pressTempToggleButton.setText("Temperature")
            self.pressTempToggleButton.setStyleSheet("background-color: rgb(255,167, 0);")
            self.pressTempToggleStatus = 'pressure'

            self.GUI_Title.setText('Pressure Monitor')

        self.toggleVisuals(True)

    def hideTempBoxes(self):
        self.temperatureValue0.hide()
        self.temperatureValue1.hide()
        self.temperatureValue2.hide()
        self.temperatureValue3.hide()

    def showTempBoxes(self):
        self.temperatureValue0.show()
        self.temperatureValue1.show()
        self.temperatureValue2.show()
        self.temperatureValue3.show()

    def setupSignals(self):
        #Hide the pressure Value initially
        self.pressureGraph.passSensor(self.pressure_sensor)
        self.pressureValue.hide()
        self.pressureUnitsLabel.hide()

        self.temperatureGraph.passSensors(self.temperature_sensors)
        self.hideTempBoxes()
        self.temperatureUnitsLabel.hide()

        #Signals
        self.showCalibrationButtons()
        self.calibrateButton.clicked.connect(lambda:self.showCalibrationButtons())
        self.numGraphToggleButton.clicked.connect(lambda:self.toggleVisuals())
        self.upperCalButton.clicked.connect(lambda:self.setUpperPoint())
        self.lowerCalButton.clicked.connect(lambda:self.setLowerPoint())
        self.logButton.clicked.connect(lambda:self.startLogging())
        self.pressTempToggleButton.clicked.connect(lambda:self.toggleTempPress())
