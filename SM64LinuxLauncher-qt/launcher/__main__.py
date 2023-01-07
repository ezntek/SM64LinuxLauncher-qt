#!/usr/bin/env python3

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

# core imports
import threading
import subprocess
import json
import os

# PyQt imports
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon

# UI imports
from uic.main_window_ui import Ui_MainWindow
from uic.about_ui import Ui_AboutDialog
from dialogs import (BuildNewDialog,
                    JsonView,
                    BuildInfo,
                    RepoInfo)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_actions()

        # data
        self.available_builds: list[str] = []
        self.refresh_builds()

        # load the repos
        with open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "./res/repos/repos.json")) as r: # get relative path
            self.repos: dict[str, dict[str, str]] = json.loads(r.read())

        self.ui.available_repos_list.addItems(self.repos.keys())
        self.ui.available_repos_list.setCurrentRow(0)

    def setup_actions(self):
        self.ui.actionQuit.triggered.connect(self.close) # connect the quit action
        self.ui.actionAbout.triggered.connect(self.about_dialog)

    def refresh_builds(self):
        try:
            for d in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./builds")):
                if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./builds", d, "./build.json")):
                    json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./builds", d, "./build.json")
                    with open(json_file_path) as json_file:
                        dic: dict = json.loads(json_file.read())
                    if dic["playable"]:
                        if d in self.available_builds:
                            return # return if already added
                        self.available_builds.append(d)
                        self.ui.builds_list.addItem(d)
                    del json_file
                    del json_file_path
                    del dic
        except FileNotFoundError:
            os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./builds"))

    def about_dialog(self):
        d = QtWidgets.QDialog(parent=None)
        u = Ui_AboutDialog()
        u.setupUi(d)
        # load the version 
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "res/version.json")) as vjson:
            v: dict = json.loads(vjson.read())
            u.label_2.setText(f"Version {v['versionMajor']}.{v['versionMinor']}.{v['versionPatch']} commit {v['commit']}")
        d.exec()
        d.close()

    # slots
    def b_build_new(self):
        selected_build = self.ui.available_repos_list.currentItem().text()
        d = BuildNewDialog(self.repos[selected_build]) # pass in the selected build
        d.exec()
        self.refresh_builds()
     
    def b_play_build(self):
        # load the build.json
        try:
            with open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                f"builds/{self.ui.builds_list.currentItem().text()}/build.json"
            )) as build_json:
                dic: dict = json.loads(build_json.read())
            
            # run the game
            game_thread = threading.Thread(target=subprocess.run, args=(f'cd \'{dic["repoRoot"]}\'; \'{dic["execPath"]}\'',), kwargs={"shell":True,})
            game_thread.start()
                
        except IndexError or AttributeError:
            pass
    
    def b_view_buildjson(self):
        try:
            selected_build = self.ui.builds_list.currentItem().text()
            d = JsonView(os.path.join(os.path.dirname(os.path.realpath(__file__)), f"./builds/{selected_build}/build.json"))
            d.exec()
        except OSError:
            print("JSON Path Invalid!!")
        except AttributeError:
            print("Build does NOT EXIST!")

    def b_build_info(self):
        try:
            selected_build = self.ui.builds_list.currentItem().text()
            BuildInfo(os.path.join(os.path.dirname(os.path.realpath(__file__)), f"./builds/{selected_build}/build.json")).exec()
        except OSError:
            print("JSON Path Invalid?")
        except AttributeError:
            print("Build does NOT EXIST!")
    
    def b_repo_info(self):
        selected_repo = self.ui.available_repos_list.currentItem().text()
        try:
            RepoInfo(self.repos[selected_repo]).exec()
        except IndexError:
            print("Cannot get selected index!")

    def b_delete_build(self):
        print("Slot got delete build")

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