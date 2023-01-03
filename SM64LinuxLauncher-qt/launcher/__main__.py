from re import I
import subprocess
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
        self.refresh_builds()

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

    def refresh_builds(self):
        for d in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./builds")):
            if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./builds", d, "./build.json")):
                json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./builds", d, "./build.json")
                with open(json_file_path) as json_file:
                    dic: dict = json.loads(json_file.read())
                if dic["playable"]:
                    self.ui.builds_list.addItem(d)
                del json_file
                del json_file_path
                del dic


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
        self.refresh_builds()
     
    def play_selected(self):
        # load the build.json
        try:
            with open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"builds/{self.ui.builds_list.currentItem().text()}/build.json"
            )) as build_json:
                dic: dict = json.loads(build_json.read())
            
            # run the game
            subprocess.run(dic["execPath"], shell=True)
        except IndexError:
            pass

# driver code

def main() -> int:
    app = QtWidgets.QApplication([])
    win = MainWindow(parent=None)
    win.show()
    return app.exec()

if __name__ == "__main__":
    exit(main())