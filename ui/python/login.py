# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/xml/login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginScreen(object):
    def setupUi(self, LoginScreen):
        LoginScreen.setObjectName("LoginScreen")
        LoginScreen.resize(935, 600)
        LoginScreen.setStyleSheet("border-top-color: rgb(76, 88, 255);\n"
"background-color: rgb(152, 193, 255);")
        self.centralwidget = QtWidgets.QWidget(LoginScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 121, 121))
        self.label.setStyleSheet("border-image: url(:/left/assets/left_logo.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 20, 611, 81))
        self.label_2.setStyleSheet("background-color: rgb(255, 227, 215);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(790, 0, 121, 121))
        self.label_3.setStyleSheet("border-image: url(:/left/assets/right_logo.png);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 140, 911, 431))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(150, 110, 631, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(150, -10, 631, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(210, 160, 541, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("\n"
"color: rgb(255, 27, 7);")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(140, 200, 731, 111))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 15, 19);")
        self.label_6.setObjectName("label_6")
        self.login_btn = QtWidgets.QPushButton(self.centralwidget)
        self.login_btn.setGeometry(QtCore.QRect(460, 500, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.login_btn.setFont(font)
        self.login_btn.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.login_btn.setObjectName("login_btn")
        LoginScreen.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LoginScreen)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 935, 26))
        self.menubar.setObjectName("menubar")
        LoginScreen.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LoginScreen)
        self.statusbar.setObjectName("statusbar")
        LoginScreen.setStatusBar(self.statusbar)

        self.retranslateUi(LoginScreen)
        QtCore.QMetaObject.connectSlotsByName(LoginScreen)

    def retranslateUi(self, LoginScreen):
        _translate = QtCore.QCoreApplication.translate
        LoginScreen.setWindowTitle(_translate("LoginScreen", "MainWindow"))
        self.label_2.setText(_translate("LoginScreen", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">HỌC VIỆN HẢI QUÂN</span></p><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">KHOA THÔNG TIN - RA ĐA</span></p></body></html>"))
        self.label_5.setText(_translate("LoginScreen", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">KHOÁ LUẬN TỐT NGHIỆP</span></p></body></html>"))
        self.label_6.setText(_translate("LoginScreen", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">NGHIÊN CỨU KHAI THÁC KỸ THUẬT PHÁT HIỆN</span></p><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">VÀ BÁM QUỸ ĐẠO MỤC TIÊU TRONG RA ĐA VRS-CSX</span></p></body></html>"))
        self.login_btn.setText(_translate("LoginScreen", "TRUY CẬP"))

import logo_rc
