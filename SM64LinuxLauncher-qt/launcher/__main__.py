from PyQt6 import QtWidgets
import json
import os
from uic.main_window_ui import Ui_MainWindow
from uic.about_ui import Ui_AboutDialog
from dialogs import BuildNewDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_actions()

        # load the repos
        with open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "./res/repos/repos.json")) as r: # get relative path
            self.repos: dict[str, dict[str, str]] = json.loads(r.read())

        self.ui.available_builds_list.addItems(self.repos.keys())      
        self.ui.available_builds_list.setCurrentRow(0)  

    def setup_actions(self):
        self.ui.action_quit.triggered.connect(self.close) # connect the quit action
        self.ui.action_about.triggered.connect(self.about_dialog)

    # Slots
    def about_dialog(self):
        d = QtWidgets.QDialog(parent=None)
        u = Ui_AboutDialog()
        u.setupUi(d)
        d.exec()
        d.close()

    def build_new(self):
        selected_build = self.ui.available_builds_list.currentItem().text()
        d = BuildNewDialog(self.repos[selected_build]) # pass in the selected build
        d.exec()
    
    def play_selected(self):
        pass

# driver code

def main() -> int:
    app = QtWidgets.QApplication([])
    app.setStyle('Breeze')
    win = MainWindow(parent=None)
    win.show()
    return app.exec()

if __name__ == "__main__":
    exit(main())