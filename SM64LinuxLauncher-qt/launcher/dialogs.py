from PyQt6 import QtWidgets
from uic.build_new_ui import Ui_BuildNewDialog
from uic.select_baserom_ui import Ui_BaseromSelectDialog

class BaseromSelectDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_BaseromSelectDialog()
        self.ui.setupUi(self)
    
    def b_continue(self):
        pass

    def select_baserom(self):
        pass


class BuildNewDialog(QtWidgets.QDialog):
    def __init__(self, repo: dict, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_BuildNewDialog()
        self.ui.setupUi(self)
        self.repo = repo
        self.ui.l_build_what.setText(repo["name"]) # set the now building label

        # data
        self.model_pack_folder = ""
        self.texture_pack_folder = ""

    # Slots
    def pick_texture_pack_folder(self):
        # create a file picker object
        picker = QtWidgets.QFileDialog(self)

        # configure and run
        picker.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        picker.exec()

        # set the lineEdit content to the picker result
        self.texture_pack_folder = picker.selectedFiles()[0]
        self.ui.texture_pack_folder.setText(picker.selectedFiles()[0])

    def pick_model_pack_folder(self):
        # create a file picker object
        picker = QtWidgets.QFileDialog(self)

        # configure and exec
        picker.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        picker.exec()

        # set the lineEdit content to the chosen folder
        self.model_pack_folder = picker.selectedFiles()[0]
        self.ui.model_pack_folder.setText(picker.selectedFiles()[0])
    
    def b_continue(self):
        dialog = BaseromSelectDialog(parent=None)
        dialog.exec()
