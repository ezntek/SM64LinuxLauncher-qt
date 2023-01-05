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


import json
import os
import git.repo
import shutil
import subprocess

from PyQt6.QtWidgets import QDialog, QWidget
from uic.failed_ui import Ui_BuildFailedDialog
from uic.succeeded_ui import Ui_BuildSucceededDialog

# class definitions
class BuildSucceededDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_BuildSucceededDialog()
        self.ui.setupUi(self)

        # data
        self.dialog_dismissed = False
        self.exec_now = False
    
    def play_now(self):
        self.dialog_dismissed = True
        self.exec_now = True
        self.close()
    
    def play_later(self):
        self.dialog_dismissed = True
        self.exec_now = False
        self.close()

# function definitions
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

def log(log: str):
    print(f"LOG: {log}")

def parse_to_dict(custom_name: str,
                  repo: dict[str, str],
                  model_pack_folder: str,
                  texture_pack_folder: str,
                  rom_path: str,
                  region: str,
                  jobs: int,
                  additional_make_opts: str) -> dict:
    
    return {
        "repo": repo,
        "usingCustomName": False if custom_name == "" else True,
        "customName": custom_name,
        "romPath": rom_path,
        "romRegion": region,
        "jobs": jobs,
        "customTextures": False if texture_pack_folder == "" else True,
        "texturesPath": texture_pack_folder,
        "customModels": False if model_pack_folder == "" else True,
        "modelsPath": model_pack_folder,
        "additionalMakeOpts": additional_make_opts,
        "playable": False,
        "execPath": ""
    }

def parse_to_json(build_dict: dict) -> str:
    return json.dumps(build_dict, indent=4, sort_keys=True)

def build(build_dict: dict):
    # put up a display in the stdout
    print("""
    +-----------------------------+
    |                             |
    | Building the Configuration. |
    | Do not close the window     |
    | OR terminal!                |
    |                             |
    +-----------------------------+
    """)
    
    # set up variables
    is_using_custom_name = build_dict["usingCustomName"]
    
    # save to build folder
    log("saving build.json...")

    new_build_folder_name = build_dict["repo"]["name"]
    if is_using_custom_name:
        new_build_folder_name = build_dict["customName"]

    if os.path.isdir(os.path.join(CURRENT_DIR, f"./builds/{new_build_folder_name}")):
        new_build_folder_name = f"Another Copy of {new_build_folder_name}"
    os.mkdir(os.path.join(CURRENT_DIR, f"./builds/{new_build_folder_name}"))
    
    # set the working folder path
    FOLDER_PATH = os.path.join(CURRENT_DIR, f"builds/{new_build_folder_name}")

    with open(os.path.join(FOLDER_PATH, "./build.json"), "w+") as buildjsonfile:
        buildjsonfile.write(parse_to_json(build_dict))

    parse_to_json(build_dict)

    # clone the repository
    log(f"cloning from {build_dict['repo']['repolink']}")
    git.repo.Repo.clone_from(
        build_dict["repo"]["repolink"],
        os.path.join(FOLDER_PATH, "repo"),
        branch=build_dict["repo"]["branchname"],
        depth=1 # save disk space by only cloning the very latest
    )

    # copy the baserom
    log(f"copying the rom from {build_dict['romPath']} to {os.path.join(FOLDER_PATH, 'repo/baserom.us.z64')}")
    shutil.copyfile(str(build_dict["romPath"]), os.path.join(FOLDER_PATH, "repo/baserom.us.z64"))

    # copy the model pack if needed
    if build_dict["customModels"]:
        log(f"copying the model pack from {build_dict['modelsPath']}")
        shutil.copytree(f"{str(build_dict['modelsPath'])}/actors", os.path.join(FOLDER_PATH, "./repo/actors"), dirs_exist_ok=True)
    
    # add EXTERNAL_DATA=1 if using custom textures
    if build_dict["customTextures"]:
        # invoke the compiler
        log(f"compiling with make EXTERNAL_DATA=1 {build_dict['additionalMakeOpts']} -j{build_dict['jobs']}")
        subprocess.run(f"""cd '{FOLDER_PATH}/repo' &&
                           make EXTERNAL_DATA=1 {build_dict['additionalMakeOpts']} -j{build_dict['jobs']}""", shell=True)
    else:
        # invoke the compiler
        log(f"compiling with make {build_dict['additionalMakeOpts']} -j{build_dict['jobs']}")
        subprocess.run(f"""cd '{FOLDER_PATH}/repo' &&
                           make {build_dict['additionalMakeOpts']} -j{build_dict['jobs']}""", shell=True)


    # copy the texture pack if needed
    if build_dict["customTextures"]:
        log(f"copying textures from {build_dict['texturesPath']}")
        shutil.copytree(os.path.join(str(build_dict['texturesPath']), "gfx"), os.path.join(FOLDER_PATH, f"repo/build/{build_dict['romRegion']}_pc/res/gfx"))
    
    # check if the executable exists
    if not os.path.exists(os.path.join(FOLDER_PATH, f"repo/build/{build_dict['romRegion']}_pc/sm64.{build_dict['romRegion']}.f3dex2e")):
        log("Build Failed: The error message should be displayed in the command output.")

        # Put up a new dialog
        d = QDialog(parent=None)
        u = Ui_BuildFailedDialog()
        u.setupUi(d)
        d.exec()
        log("Exiting to main menu...")
        
        # delete the variables
        del d, u
        return

    log("Build Succeeded. Adding Entry to Builds List...")

    # Add the new build entry to the builds list
    build_dict["playable"] = True
    build_dict["repoRoot"] = os.path.join(FOLDER_PATH, "repo") # this is to allow for cding to the root of the repo to fix the libdiscord_game_sdk.so error
    build_dict["execPath"] = os.path.join(FOLDER_PATH, f"repo/build/{build_dict['romRegion']}_pc/sm64.{build_dict['romRegion']}.f3dex2e")

    # save the dict
    os.remove(os.path.join(FOLDER_PATH, "./build.json"))

    with open(os.path.join(FOLDER_PATH, "./build.json"), "w+") as buildjsonfile:
        buildjsonfile.write(parse_to_json(build_dict))

    # open the build succeeded dialog

    build_succeeded_dialog = BuildSucceededDialog(parent=None)
    
    while not build_succeeded_dialog.dialog_dismissed:
        build_succeeded_dialog.exec()
        if build_succeeded_dialog.dialog_dismissed:
            if build_succeeded_dialog.play_now:
                subprocess.run(build_dict["execPath"])
                build_succeeded_dialog.close()
                break
            
            # break if not playing now
            build_succeeded_dialog.close()
            break

    del build_succeeded_dialog

    # exit
    return 