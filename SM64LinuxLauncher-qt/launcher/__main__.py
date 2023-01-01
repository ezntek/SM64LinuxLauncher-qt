from PyQt5 import QtWidgets
import json
import os
from uic.main_window_ui import Ui_MainWindow
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
                "./repos/available_repos.json")) as r: # get relative path
            self.repos = json.loads(r.read())
        
        for key in self.repos.keys():
            self.ui.available_builds_list.addItem(key)

    def setup_actions(self):
        self.ui.action_quit.triggered.connect(self.close) # connect the quit action

    # Slots
    def build_new(self):
        selected_build = self.ui.available_builds_list.currentItem().text()
        d = BuildNewDialog(self.repos[selected_build]) # pass in the selected build
        d.exec()
    
    def play_selected(self):
        pass

# driver code

def main() -> int:
    app = QtWidgets.QApplication([])
    win = MainWindow(parent=None)
    win.show()
    return app.exec()

if __name__ == "__main__":
    exit(main())