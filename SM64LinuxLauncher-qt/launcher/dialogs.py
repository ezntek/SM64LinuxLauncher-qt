from PyQt6 import QtWidgets
import os
import json 

# UIs
from uic.build_new_ui import Ui_BuildNewDialog
from uic.select_baserom_ui import Ui_BaseromSelectDialog
from uic.flags_ui import Ui_BuildFlagsDialog
from uic.recheck_config_ui import Ui_RecheckConfigurationDialog

class BaseromSelectDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_BaseromSelectDialog()
        self.ui.setupUi(self)

        self.rom_path = ""
        self.region = ""
    
    def b_continue(self):
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
            self.close()

    def select_baserom(self):
        # create the file picker object
        picker = QtWidgets.QFileDialog(self)
        picker.setNameFilters(["Nintendo 64 ROMs (*.z64)"])
        picker.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        picker.exec()

        # update the lineEdit contents
        self.ui.baserom_path.setText(picker.selectedFiles()[0])

        # set the rom path
        self.rom_path = picker.selectedFiles()[0]

class BuildFlagsDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_BuildFlagsDialog()
        self.ui.setupUi(self)

        # data
        self.jobs: int = 0
        self.additional_make_opts = ""
    
    def start_build(self):
        if int(self.ui.jobs.currentText()) == 0:
            self.jobs = 4 # set the default
        else:
            self.jobs = int(self.ui.jobs.currentText())
         
        self.additional_make_opts = self.ui.flags.text()
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

    def load_values(self):
        # load available repos
        index = 0 # for setting the current index
        with open(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "./repos/repos.json"
        )) as r:
            repos_dict: dict = json.loads(r.read())
            for count, repo_name in enumerate(repos_dict.keys()):
                self.ui.combobox_repo.addItem(repo_name)
                if repo_name == self.repo["name"]:
                    index = count

        self.ui.combobox_repo.setCurrentIndex(index)

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
    def b_build(self):
        pass

    def b_baserom_path(self):
        pass
    
    def b_modelpack_path(self):
        pass
    
    def b_texturepack_path(self):
        pass


class BuildNewDialog(QtWidgets.QDialog):
    def __init__(self, repo: dict, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_BuildNewDialog()
        self.ui.setupUi(self)
        self.repo = repo
        self.custom_name = ""
        self.ui.l_build_what.setText(repo["name"]) # set the now building label

        # data
        self.model_pack_folder = ""
        self.texture_pack_folder = ""
        self.rom_path = ""
        self.region = ""
        self.jobs: int = 0
        self.additional_make_opts = ""

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
        # set custom name
        self.custom_name = self.ui.repo_custom_name.text()

        # select BaseROM
        baserom_dialog = BaseromSelectDialog(parent=None)
        baserom_dialog.exec()

        self.rom_path, self.region = baserom_dialog.rom_path, baserom_dialog.region # set the values
        del baserom_dialog # delete to free memory

        # select Flags
        flags_dialog = BuildFlagsDialog(parent=None)
        flags_dialog.exec()

        # set the values
        self.jobs, self.additional_make_opts = flags_dialog.jobs, flags_dialog.additional_make_opts
        del flags_dialog # delete the instance

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
        recheck_val_dialog.exec()

         
