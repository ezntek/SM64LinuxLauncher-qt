# Form implementation generated from reading ui file './SM64LinuxLauncher-qt/launcher/res/ui/flags.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_BuildFlagsDialog(object):
    def setupUi(self, BuildFlagsDialog):
        BuildFlagsDialog.setObjectName("BuildFlagsDialog")
        BuildFlagsDialog.resize(599, 219)
        self.gridLayout = QtWidgets.QGridLayout(BuildFlagsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.l_flags = QtWidgets.QLabel(BuildFlagsDialog)
        self.l_flags.setObjectName("l_flags")
        self.gridLayout.addWidget(self.l_flags, 2, 0, 1, 1)
        self.jobs = QtWidgets.QComboBox(BuildFlagsDialog)
        self.jobs.setObjectName("jobs")
        self.jobs.addItem("")
        self.jobs.addItem("")
        self.jobs.addItem("")
        self.jobs.addItem("")
        self.jobs.addItem("")
        self.jobs.addItem("")
        self.jobs.addItem("")
        self.gridLayout.addWidget(self.jobs, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        self.l_jobs = QtWidgets.QLabel(BuildFlagsDialog)
        self.l_jobs.setObjectName("l_jobs")
        self.gridLayout.addWidget(self.l_jobs, 1, 0, 1, 2)
        self.flags = QtWidgets.QLineEdit(BuildFlagsDialog)
        self.flags.setObjectName("flags")
        self.gridLayout.addWidget(self.flags, 2, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.start_build = QtWidgets.QPushButton(BuildFlagsDialog)
        self.start_build.setObjectName("start_build")
        self.gridLayout.addWidget(self.start_build, 4, 2, 1, 1)
        self.b_cancel = QtWidgets.QPushButton(BuildFlagsDialog)
        self.b_cancel.setObjectName("b_cancel")
        self.gridLayout.addWidget(self.b_cancel, 4, 1, 1, 1)

        self.retranslateUi(BuildFlagsDialog)
        self.start_build.clicked.connect(BuildFlagsDialog.start_build) # type: ignore
        self.b_cancel.clicked.connect(BuildFlagsDialog.b_cancel) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(BuildFlagsDialog)

    def retranslateUi(self, BuildFlagsDialog):
        _translate = QtCore.QCoreApplication.translate
        BuildFlagsDialog.setWindowTitle(_translate("BuildFlagsDialog", "Set Misc. Options"))
        self.l_flags.setText(_translate("BuildFlagsDialog", "Additional Build Flags (Leave Blank If Unsure)"))
        self.jobs.setItemText(0, _translate("BuildFlagsDialog", "4"))
        self.jobs.setItemText(1, _translate("BuildFlagsDialog", "1"))
        self.jobs.setItemText(2, _translate("BuildFlagsDialog", "2"))
        self.jobs.setItemText(3, _translate("BuildFlagsDialog", "8"))
        self.jobs.setItemText(4, _translate("BuildFlagsDialog", "10"))
        self.jobs.setItemText(5, _translate("BuildFlagsDialog", "12"))
        self.jobs.setItemText(6, _translate("BuildFlagsDialog", "16"))
        self.l_jobs.setText(_translate("BuildFlagsDialog", "No. Of Concurrent Jobs (pick 4 if unsure)"))
        self.start_build.setText(_translate("BuildFlagsDialog", "Continue"))
        self.b_cancel.setText(_translate("BuildFlagsDialog", "Cancel"))
