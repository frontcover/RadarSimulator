# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/xml/ui_main_screen.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainScreen(object):
    def setupUi(self, MainScreen):
        MainScreen.setObjectName("MainScreen")
        MainScreen.resize(878, 660)
        self.radar = Radar(MainScreen)
        self.radar.setGeometry(QtCore.QRect(60, 90, 500, 500))
        self.radar.setObjectName("radar")
        self.label = QtWidgets.QLabel(MainScreen)
        self.label.setGeometry(QtCore.QRect(20, 40, 79, 31))
        self.label.setObjectName("label")
        self.lineEdit_kc = QtWidgets.QLineEdit(MainScreen)
        self.lineEdit_kc.setGeometry(QtCore.QRect(110, 40, 71, 22))
        self.lineEdit_kc.setObjectName("lineEdit_kc")
        self.label_2 = QtWidgets.QLabel(MainScreen)
        self.label_2.setGeometry(QtCore.QRect(200, 40, 55, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_pv = QtWidgets.QLineEdit(MainScreen)
        self.lineEdit_pv.setGeometry(QtCore.QRect(270, 40, 71, 22))
        self.lineEdit_pv.setObjectName("lineEdit_pv")
        self.label_3 = QtWidgets.QLabel(MainScreen)
        self.label_3.setGeometry(QtCore.QRect(370, 40, 55, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_hd = QtWidgets.QLineEdit(MainScreen)
        self.lineEdit_hd.setGeometry(QtCore.QRect(430, 40, 71, 22))
        self.lineEdit_hd.setObjectName("lineEdit_hd")
        self.label_4 = QtWidgets.QLabel(MainScreen)
        self.label_4.setGeometry(QtCore.QRect(510, 50, 55, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_vt = QtWidgets.QLineEdit(MainScreen)
        self.lineEdit_vt.setGeometry(QtCore.QRect(570, 40, 71, 22))
        self.lineEdit_vt.setObjectName("lineEdit_vt")
        self.btn_create = QtWidgets.QPushButton(MainScreen)
        self.btn_create.setGeometry(QtCore.QRect(670, 40, 93, 28))
        self.btn_create.setObjectName("btn_create")

        self.retranslateUi(MainScreen)
        QtCore.QMetaObject.connectSlotsByName(MainScreen)

    def retranslateUi(self, MainScreen):
        _translate = QtCore.QCoreApplication.translate
        MainScreen.setWindowTitle(_translate("MainScreen", "Form"))
        self.label.setText(_translate("MainScreen", "Khoảng cách"))
        self.label_2.setText(_translate("MainScreen", "Phương vị"))
        self.label_3.setText(_translate("MainScreen", "Hướng đi"))
        self.label_4.setText(_translate("MainScreen", "Vận tốc"))
        self.btn_create.setText(_translate("MainScreen", "Tạo"))

from radar import Radar
