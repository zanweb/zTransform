# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zConvert.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(794, 229)
        font = QtGui.QFont()
        font.setPointSize(9)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit_NCPath = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_NCPath.setGeometry(QtCore.QRect(120, 50, 441, 20))
        self.lineEdit_NCPath.setObjectName("lineEdit_NCPath")
        self.label_NcPath = QtWidgets.QLabel(self.centralwidget)
        self.label_NcPath.setGeometry(QtCore.QRect(30, 50, 81, 20))
        self.label_NcPath.setObjectName("label_NcPath")
        self.label_ConvertPatch = QtWidgets.QLabel(self.centralwidget)
        self.label_ConvertPatch.setGeometry(QtCore.QRect(30, 90, 81, 21))
        self.label_ConvertPatch.setObjectName("label_ConvertPatch")
        self.lineEdit_ConvertPath = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_ConvertPath.setGeometry(QtCore.QRect(120, 90, 441, 20))
        self.lineEdit_ConvertPath.setObjectName("lineEdit_ConvertPath")
        self.pushButton_NCPath = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_NCPath.setGeometry(QtCore.QRect(580, 50, 131, 23))
        self.pushButton_NCPath.setObjectName("pushButton_NCPath")
        self.pushButton_ConvertPath = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ConvertPath.setGeometry(QtCore.QRect(580, 90, 131, 23))
        self.pushButton_ConvertPath.setObjectName("pushButton_ConvertPath")
        self.pushButton_Run = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Run.setGeometry(QtCore.QRect(720, 50, 61, 61))
        self.pushButton_Run.setObjectName("pushButton_Run")
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(290, 10, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(430, 140, 341, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(490, 20, 181, 16))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 794, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "zConvert"))
        self.label_NcPath.setText(_translate("MainWindow", "NC File Path:"))
        self.label_ConvertPatch.setText(_translate("MainWindow", "Convert Path:"))
        self.pushButton_NCPath.setText(_translate("MainWindow", "Browse NC Path"))
        self.pushButton_ConvertPath.setText(_translate("MainWindow", "Browse Convert Path"))
        self.pushButton_Run.setText(_translate("MainWindow", "Run"))
        self.label_title.setText(_translate("MainWindow", "zConvert"))
        self.label.setText(_translate("MainWindow", "Made by: Zhan, Yongqiang Ver:Beta Date:2018.5.18"))
        self.label_2.setText(_translate("MainWindow", "NC Convert to MFG code"))

