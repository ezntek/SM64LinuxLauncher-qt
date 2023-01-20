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

import threading
import json
import os
import build

from PyQt6 import QtWidgets

# UIs
from uic.build_new_ui import Ui_BuildNewDialog
from uic.select_baserom_ui import Ui_BaseromSelectDialog
from uic.flags_ui import Ui_BuildFlagsDialog
from uic.recheck_config_ui import Ui_RecheckConfigurationDialog
from uic.view_json_ui import Ui_PlainTextView
from uic.info_ui import Ui_InfoDialog
from uic.repo_info_ui import Ui_RepoInfoDialog
from uic.confirm_delete_ui import Ui_ConfirmDeleteDialog

class ConfirmDelete(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_ConfirmDeleteDialog()
        self.ui.setupUi(self)

        # data
        self.delete: bool
    
    def b_yes(self):
        self.delete = True
        self.close()
    
    def b_no(self):
        self.delete = False
        self.close()
class RepoInfo(QtWidgets.QDialog):
    def __init__(self, repo_dict: dict, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        # setup UI
        self.ui = Ui_RepoInfoDialog() 
        self.ui.setupUi(self)

        # data
        self.repo_dict: dict = repo_dict
        self.load_data()
    
    def load_data(self):
        self.ui.repo_link.setText(self.repo_dict["repolink"])
        self.ui.repo_name.setText(self.repo_dict["name"])
        self.ui.repo_branch.setText(self.repo_dict["branchname"])

    def b_ok(self):
        self.close()

class BuildInfo(QtWidgets.QDialog):
    def __init__(self, json_path: str, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        # setupUI
        self.ui = Ui_InfoDialog()
        self.ui.setupUi(self)

        # data
        self.build: dict
        self.build_json_path: str = json_path
        self.load_data()
    
    def load_data(self):
        try:
            with open(self.build_json_path, "r+") as buildjson:
                self.build = json.loads(buildjson.read())
        except OSError:
            print("Error loading the build.json!")
            raise OSError

        self.ui.repo_name.setText(self.build["repo"]["name"])
        self.ui.custom_name.setText(self.build["customName"]) if self.build["customName"] != "" else None
        self.ui.region.setText(self.build["romRegion"])
        self.ui.textures.setText(str(self.build["customTextures"]))
        self.ui.models.setText(str(self.build["customModels"]))
        self.ui.exec_path.setText(self.build["execPath"])
    
    # slots
    def b_ok(self):
        self.close()

class JsonView(QtWidgets.QDialog):
    def __init__(self, json_path: str, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        # setup the UI
        self.ui = Ui_PlainTextView()
        self.ui.setupUi(self)

        # data
        self.text: str
        self.path = json_path
        self.init_json()

    def init_json(self):
        try:
            with open(self.path, "r+") as jsonfile:
                self.text = jsonfile.read()
                self.ui.plainTextEdit.setPlainText(self.text)
                self.setWindowTitle("View build.json")
        except OSError:
            print("The File Path is probably invalid!")
            raise OSError
    
    # slots
    def b_ok(self):
        self.close()

class BaseromSelectDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_BaseromSelectDialog()
        self.ui.setupUi(self)

        self.dialog_dismissed = False
        self.cancelled_build_job = False
        self.rom_path = ""
        self.region = ""
    
    # slots
    def b_cancel(self):
        self.cancelled_build_job = True
        self.close()

    def b_continue(self):
        self.rom_path = self.ui.baserom_path.text() # Sync the UI and backend in case if the user cleared the path
        match self.ui.region_select.currentText:
            case "USA (us)":
                self.region = "us"
            case "Japanese (jp)":
                self.region = "jp"
            case "European PAL (eu)":
                self.region = "eu"
            case default:
                self.region = "us"
        if self.rom_path == "":
            dialog = QtWidgets.QDialog() # build a new dialog

            # set the grid layout
            grid_layout = QtWidgets.QGridLayout(dialog)

            # add a label
            label = QtWidgets.QLabel(dialog)
            label.setText("Please select a valid ROM Path before continuing!")
            grid_layout.addWidget(label, 0, 0, 0, 1)

            # add a button
            button = QtWidgets.QPushButton(dialog)
            button.setText("OK")
            button.clicked.connect(dialog.close)
            grid_layout.addWidget(button, 1, 1)

            # show the dialog
            dialog.exec()
        else:
            self.dialog_dismissed = True
            self.close()

    def select_baserom(self):
        # create the file picker object
        picker = QtWidgets.QFileDialog(self)
        picker.setNameFilters(["Nintendo 64 ROMs (*.z64)"])
        picker.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        picker.exec()

        try:
            # update the lineEdit contents
            self.ui.baserom_path.setText(picker.selectedFiles()[0])

            # set the rom path
            self.rom_path = picker.selectedFiles()[0]
            del picker
        except IndexError:
            del picker
            return

    def exec(self) -> int:
        self.dialog_dismissed = False
        return super().exec()

class BuildFlagsDialog(QtWidgets.QDialog):    
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_BuildFlagsDialog()
        self.ui.setupUi(self)

        self.dialog_dismissed = False
        self.cancelled_build_job = False
        # data
        self.jobs: int = 0
        self.additional_make_opts = ""

    # reset the variable on each launch
    def exec(self) -> int:
        self.dialog_dismissed = False
        return super().exec()

    # slots
    def b_cancel(self):
        self.cancelled_build_job = True
        self.close()

    def start_build(self):
        if int(self.ui.jobs.currentText()) == 0:
            self.jobs = 4 # set the default
        else:
            self.jobs = int(self.ui.jobs.currentText())
         
        self.additional_make_opts = self.ui.flags.text()
        self.dialog_dismissed = True
        self.close()

class RecheckConfigDialog(QtWidgets.QDialog):
    def __init__(self,
                    custom_name: str,
                    repo: dict[str, str],
                    model_pack_folder: str,
                    texture_pack_folder: str,
                    rom_path: str,
                    region: str,
                    jobs: int,
                    additional_make_opts: str,
                    parent: QtWidgets.QWidget | None = None) -> None:

        super().__init__(parent)
        self.ui = Ui_RecheckConfigurationDialog()
        self.ui.setupUi(self)
        self.dialog_dismissed = False
        self.cancelled_build_job = False

        # set values as class members
        self.custom_name = custom_name
        self.repo = repo
        self.model_pack_folder = model_pack_folder
        self.texture_pack_folder = texture_pack_folder
        self.rom_path = rom_path
        self.region = region
        self.jobs = jobs
        self.additional_make_opts = additional_make_opts

        # load values into UI
        self.load_values()

    # reset the variable on dialog open
    def exec(self) -> int:
        self.dialog_dismissed = False
        return super().exec()

    def load_values(self):
        # load repo
        self.ui.l_repo_display.setText(self.repo["name"])

        # load base rom path
        self.ui.line_edit_baserom_path.setText(self.rom_path)

        # load base rom region        
        self.ui.combobox_romregion.setCurrentIndex({
            "us": 0,
            "eu": 1,
            "jp": 2
        }[self.region]) # set indexes based on region

        # set custom name
        self.ui.line_edit_custom_name.setText(self.custom_name)

        # jobs
        self.ui.combobox_jobs.setCurrentIndex({
            4: 0,
            1: 1,
            2: 2,
            8: 3,
            10: 4,
            12: 5,
            16: 6
        }[self.jobs]) # dict[Jobs, Index]

        # additional MAKEOPTS
        self.ui.line_edit_build_flags.setText(self.additional_make_opts)

        # texture pack
        self.ui.line_edit_texture_pack.setText(self.texture_pack_folder)

        # model pack
        self.ui.line_edit_model_pack.setText(self.model_pack_folder)

    
    # slots
    def b_cancel(self):
        self.cancelled_build_job = True
        self.close()

    
    def b_build(self):
        # sync the UI elements before exiting
        self.texture_pack_folder = self.ui.line_edit_texture_pack.text()
        self.model_pack_folder = self.ui.line_edit_model_pack.text()

        # exit
        self.dialog_dismissed = True
        self.close()

    
    def b_baserom_path(self):
        # Create new Dialog
        file_sel = QtWidgets.QFileDialog()
        file_sel.setNameFilter("Nintendo 64 ROMs (*.z64)")
        file_sel.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        file_sel.exec()

        # Update UI
        try:
            self.rom_path = file_sel.selectedFiles()[0]
            self.ui.line_edit_baserom_path.setText(self.rom_path)
            del file_sel
        except IndexError: # if there is an IndexError, that means the file picker was closed abruptly
            del file_sel # delete to free memory
            return

        
    def b_modelpack_path(self):
        # create new File Picker Dialog
        modelpack_sel = QtWidgets.QFileDialog()
        modelpack_sel.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        modelpack_sel.exec()

        # Update UI
        try:
            self.model_pack_folder = modelpack_sel.selectedFiles()[0]
            self.ui.line_edit_model_pack.setText(self.model_pack_folder)
            del modelpack_sel
        except IndexError:
            del modelpack_sel
            return

        
    def b_texturepack_path(self):
        texturepack_sel = QtWidgets.QFileDialog()
        texturepack_sel.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        texturepack_sel.exec()

        try:
            self.texture_pack_folder = texturepack_sel.selectedFiles()[0]
            self.ui.line_edit_texture_pack.setText(self.texture_pack_folder)
        except IndexError:
            del texturepack_sel
            return

class BuildNewDialog(QtWidgets.QDialog):
    def __init__(self, repo: dict, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_BuildNewDialog()
        self.ui.setupUi(self)
        self.repo: dict[str, str] = repo
        self.custom_name = ""
        self.ui.l_build_what.setText(repo["name"]) # set the now building label

        # data
        self.model_pack_folder = ""
        self.texture_pack_folder = ""
        self.rom_path = ""
        self.region = ""
        self.jobs: int = 0
        self.additional_make_opts = ""

        # make builds folder if it doesnt exist already
        if not os.path.isdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./builds")):
            os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./builds"))


    # Slots
    def b_cancel(self):
        self.close()
        del self
        return

    def pick_texture_pack_folder(self):
        # create a file picker object
        picker = QtWidgets.QFileDialog(self)

        # configure and run
        picker.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        picker.exec()

        try:
            # set the lineEdit content to the picker result
            self.texture_pack_folder = picker.selectedFiles()[0]
            self.ui.texture_pack_folder.setText(picker.selectedFiles()[0])
            del picker
        except IndexError:
            del picker
            return

    def pick_model_pack_folder(self):
        # create a file picker object
        picker = QtWidgets.QFileDialog(self)

        # configure and exec
        picker.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        picker.exec()

        try:
            # set the lineEdit content to the chosen folder
            self.model_pack_folder = picker.selectedFiles()[0]
            self.ui.model_pack_folder.setText(picker.selectedFiles()[0])
            del picker
        except IndexError:
            del picker
            return

    def b_continue(self):
        # set custom name
        self.custom_name = self.ui.repo_custom_name.text()

        # Sync UI elements with backend
        self.model_pack_folder = self.ui.model_pack_folder.text()
        self.texture_pack_folder = self.ui.texture_pack_folder.text()

        # select BaseROM
        baserom_dialog = BaseromSelectDialog(parent=None)

        # start the loop and break if properly dismissed
        while not baserom_dialog.dialog_dismissed:
            baserom_dialog.exec()
            if baserom_dialog.cancelled_build_job:
                del baserom_dialog
                self.close()
                return
            if baserom_dialog.dialog_dismissed:
                self.rom_path, self.region = baserom_dialog.rom_path, baserom_dialog.region
                del baserom_dialog
                break

        # select Flags
        flags_dialog: BuildFlagsDialog = BuildFlagsDialog(parent=None)

        # start a loop and break if properly dismissed
        while not flags_dialog.dialog_dismissed:
            flags_dialog.exec()
            if flags_dialog.cancelled_build_job:
                del flags_dialog
                self.close()
                return
            if flags_dialog.dialog_dismissed:
                self.jobs, self.additional_make_opts = flags_dialog.jobs, flags_dialog.additional_make_opts
                del flags_dialog # delete the instance
                break

        # Recheck Values Dialog
        recheck_val_dialog = RecheckConfigDialog(
            self.custom_name,
            self.repo,
            self.model_pack_folder,
            self.texture_pack_folder,
            self.rom_path,
            self.region,
            self.jobs,
            self.additional_make_opts,
            parent=None
        )

        while not recheck_val_dialog.dialog_dismissed:
            recheck_val_dialog.exec()
            if recheck_val_dialog.cancelled_build_job:
                del recheck_val_dialog
                self.close()
                return
            if recheck_val_dialog.dialog_dismissed:
                # set the new values
                (self.custom_name, self.model_pack_folder,
                self.texture_pack_folder, self.rom_path,
                self.region, self.jobs, self.additional_make_opts) = (
                    recheck_val_dialog.custom_name, recheck_val_dialog.model_pack_folder,
                    recheck_val_dialog.texture_pack_folder, recheck_val_dialog.rom_path,
                    recheck_val_dialog.region, recheck_val_dialog.jobs, recheck_val_dialog.additional_make_opts
                )

        self.close()

        build_process = threading.Thread(target=build.build, args=(build.parse_to_dict(
            self.custom_name,
            self.repo,
            self.model_pack_folder,
            self.texture_pack_folder,
            self.rom_path,
            self.region,
            self.jobs,
            self.additional_make_opts
        ),))

        build_process.start()

        return
