# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
import sys
# from Ui_MainWindow import Ui_MainWindow
from MainUi import MainUi
from Sensor import PressureSensor, TemperatureSensor

# import numpy as np
# import pyqtgraph as pg

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        pressureSensor = PressureSensor()
        Therms = [TemperatureSensor(), TemperatureSensor(), TemperatureSensor(), TemperatureSensor()]
        self.ui = MainUi(pressureSensor, Therms)
        self.ui.setupUi(self)
        self.ui.setupSignals()
        # self.move(-3,-30)

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
