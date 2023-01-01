from PyQt5 import QtWidgets
from uic.build_new_ui import Ui_BuildNewDialog

class BuildNewDialog(QtWidgets.QDialog):
    def __init__(self, repo: dict, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_BuildNewDialog()
        self.ui.setupUi(self)
        self.repo = repo
        self.ui.l_build_what.setText(repo["name"]) # set the now building label

    # Slots
    def pick_texture_pack_folder(self):
        print("Recieved Texture Pack select!")
    
    def pick_model_pack_folder(self):
        print("Recieved Model Pack Select!")
    
    def b_continue(self):
        print("Recieved Continue!")
