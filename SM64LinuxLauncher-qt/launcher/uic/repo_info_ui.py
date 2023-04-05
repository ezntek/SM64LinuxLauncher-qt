# Form implementation generated from reading ui file './SM64LinuxLauncher-qt/launcher/res/ui/repo_info.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RepoInfoDialog(object):
    def setupUi(self, RepoInfoDialog):
        RepoInfoDialog.setObjectName("RepoInfoDialog")
        RepoInfoDialog.resize(429, 300)
        self.gridLayout = QtWidgets.QGridLayout(RepoInfoDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.repo_link = QtWidgets.QLineEdit(RepoInfoDialog)
        self.repo_link.setReadOnly(True)
        self.repo_link.setObjectName("repo_link")
        self.gridLayout.addWidget(self.repo_link, 1, 2, 1, 2)
        self.repo_name = QtWidgets.QLineEdit(RepoInfoDialog)
        self.repo_name.setReadOnly(True)
        self.repo_name.setObjectName("repo_name")
        self.gridLayout.addWidget(self.repo_name, 0, 2, 1, 2)
        self.l_repo_link = QtWidgets.QLabel(RepoInfoDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.l_repo_link.setFont(font)
        self.l_repo_link.setObjectName("l_repo_link")
        self.gridLayout.addWidget(self.l_repo_link, 1, 0, 1, 1)
        self.l_repo_branch = QtWidgets.QLabel(RepoInfoDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.l_repo_branch.setFont(font)
        self.l_repo_branch.setObjectName("l_repo_branch")
        self.gridLayout.addWidget(self.l_repo_branch, 2, 0, 1, 1)
        self.repo_branch = QtWidgets.QLineEdit(RepoInfoDialog)
        self.repo_branch.setReadOnly(True)
        self.repo_branch.setObjectName("repo_branch")
        self.gridLayout.addWidget(self.repo_branch, 2, 2, 1, 2)
        self.b_ok = QtWidgets.QPushButton(RepoInfoDialog)
        self.b_ok.setObjectName("b_ok")
        self.gridLayout.addWidget(self.b_ok, 3, 3, 1, 1)
        self.l_repo_name = QtWidgets.QLabel(RepoInfoDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.l_repo_name.setFont(font)
        self.l_repo_name.setObjectName("l_repo_name")
        self.gridLayout.addWidget(self.l_repo_name, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 2, 1, 1)

        self.retranslateUi(RepoInfoDialog)
        self.b_ok.clicked.connect(RepoInfoDialog.b_ok) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(RepoInfoDialog)

    def retranslateUi(self, RepoInfoDialog):
        _translate = QtCore.QCoreApplication.translate
        RepoInfoDialog.setWindowTitle(_translate("RepoInfoDialog", "Repository Info"))
        self.l_repo_link.setText(_translate("RepoInfoDialog", "Repo Link"))
        self.l_repo_branch.setText(_translate("RepoInfoDialog", "Repo Branch"))
        self.b_ok.setText(_translate("RepoInfoDialog", "Ok"))
        self.l_repo_name.setText(_translate("RepoInfoDialog", "Repo Name"))