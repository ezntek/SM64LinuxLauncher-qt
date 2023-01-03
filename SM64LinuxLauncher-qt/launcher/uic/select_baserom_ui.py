# Form implementation generated from reading ui file './SM64LinuxLauncher-qt/launcher/res/ui/select_baserom.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_BaseromSelectDialog(object):
    def setupUi(self, BaseromSelectDialog):
        BaseromSelectDialog.setObjectName("BaseromSelectDialog")
        BaseromSelectDialog.resize(499, 155)
        self.gridLayout = QtWidgets.QGridLayout(BaseromSelectDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.browse_baserom = QtWidgets.QPushButton(BaseromSelectDialog)
        self.browse_baserom.setObjectName("browse_baserom")
        self.gridLayout.addWidget(self.browse_baserom, 0, 2, 1, 1)
        self.baserom_path = QtWidgets.QLineEdit(BaseromSelectDialog)
        self.baserom_path.setReadOnly(True)
        self.baserom_path.setClearButtonEnabled(False)
        self.baserom_path.setObjectName("baserom_path")
        self.gridLayout.addWidget(self.baserom_path, 0, 1, 1, 1)
        self.l_region_select = QtWidgets.QLabel(BaseromSelectDialog)
        self.l_region_select.setObjectName("l_region_select")
        self.gridLayout.addWidget(self.l_region_select, 1, 0, 1, 1)
        self.l_baserom_select = QtWidgets.QLabel(BaseromSelectDialog)
        self.l_baserom_select.setObjectName("l_baserom_select")
        self.gridLayout.addWidget(self.l_baserom_select, 0, 0, 1, 1)
        self.clear_baserom = QtWidgets.QPushButton(BaseromSelectDialog)
        self.clear_baserom.setObjectName("clear_baserom")
        self.gridLayout.addWidget(self.clear_baserom, 0, 3, 1, 1)
        self.region_select = QtWidgets.QComboBox(BaseromSelectDialog)
        self.region_select.setObjectName("region_select")
        self.region_select.addItem("")
        self.region_select.addItem("")
        self.region_select.addItem("")
        self.gridLayout.addWidget(self.region_select, 1, 2, 1, 2)
        self.b_continue = QtWidgets.QPushButton(BaseromSelectDialog)
        self.b_continue.setObjectName("b_continue")
        self.gridLayout.addWidget(self.b_continue, 3, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 3, 1, 1)
        self.b_cancel = QtWidgets.QPushButton(BaseromSelectDialog)
        self.b_cancel.setObjectName("b_cancel")
        self.gridLayout.addWidget(self.b_cancel, 3, 2, 1, 1)

        self.retranslateUi(BaseromSelectDialog)
        self.browse_baserom.clicked.connect(BaseromSelectDialog.select_baserom) # type: ignore
        self.b_continue.clicked.connect(BaseromSelectDialog.b_continue) # type: ignore
        self.clear_baserom.clicked.connect(self.baserom_path.clear) # type: ignore
        self.b_cancel.clicked.connect(BaseromSelectDialog.b_cancel) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(BaseromSelectDialog)

    def retranslateUi(self, BaseromSelectDialog):
        _translate = QtCore.QCoreApplication.translate
        BaseromSelectDialog.setWindowTitle(_translate("BaseromSelectDialog", "Select Base ROM"))
        self.browse_baserom.setText(_translate("BaseromSelectDialog", "Browse"))
        self.l_region_select.setText(_translate("BaseromSelectDialog", "Select the Region"))
        self.l_baserom_select.setText(_translate("BaseromSelectDialog", "Select A Base ROM"))
        self.clear_baserom.setText(_translate("BaseromSelectDialog", "Clear"))
        self.region_select.setItemText(0, _translate("BaseromSelectDialog", "USA (us)"))
        self.region_select.setItemText(1, _translate("BaseromSelectDialog", "European PAL (eu)"))
        self.region_select.setItemText(2, _translate("BaseromSelectDialog", "Japanese (jp)"))
        self.b_continue.setText(_translate("BaseromSelectDialog", "Continue"))
        self.b_cancel.setText(_translate("BaseromSelectDialog", "Cancel"))
