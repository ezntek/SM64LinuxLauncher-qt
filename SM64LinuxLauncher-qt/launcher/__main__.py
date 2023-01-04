#    SM64LinuxLauncher-qt 
#    A rewrite of SM64LinuxLauncher in PyQt that aims to improve user experience.

#    Copyright (C) 2023 ezntek (ezntek@xflymusic.com)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/.

import subprocess
import json
import os

from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
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
        try:
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
        except FileNotFoundError:
            os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./builds"))

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
            subprocess.run(dic["execPath"])
        except IndexError:
            pass

# driver code

def main() -> int:
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QIcon(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "./res/img/logo.png"
        )
    ))
    win = MainWindow(parent=None)
    win.show()
    return app.exec()

if __name__ == "__main__":
    exit(main())