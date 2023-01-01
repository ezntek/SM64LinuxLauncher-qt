# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './SM64LinuxLauncher-qt/launcher/ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(779, 595)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.available_builds_list = QtWidgets.QListWidget(self.centralwidget)
        self.available_builds_list.setObjectName("available_builds_list")
        self.gridLayout.addWidget(self.available_builds_list, 9, 4, 1, 1)
        self.build_button = QtWidgets.QPushButton(self.centralwidget)
        self.build_button.setObjectName("build_button")
        self.gridLayout.addWidget(self.build_button, 0, 4, 1, 1)
        self.builds_list = QtWidgets.QListWidget(self.centralwidget)
        self.builds_list.setObjectName("builds_list")
        self.gridLayout.addWidget(self.builds_list, 9, 2, 4, 1)
        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setObjectName("play_button")
        self.gridLayout.addWidget(self.play_button, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 779, 29))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.action_quit = QtWidgets.QAction(MainWindow)
        self.action_quit.setObjectName("action_quit")
        self.menuFile.addAction(self.action_quit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.build_button.clicked.connect(MainWindow.build_new) # type: ignore
        self.play_button.clicked.connect(MainWindow.play_selected) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SM64LinuxLauncher"))
        self.build_button.setText(_translate("MainWindow", "Build New"))
        self.play_button.setText(_translate("MainWindow", "Play"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.action_quit.setText(_translate("MainWindow", "Quit"))
