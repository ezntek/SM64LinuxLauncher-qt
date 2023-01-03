import json
import os
from typing import Any
import git.repo
import shutil
import subprocess

from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel
from uic.building_ui import Ui_BuildingDialog

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

def new_text_dialog(text: str):
    dialog = QDialog(parent=None)
    grid = QGridLayout(dialog)
    label = QLabel(text)
    grid.addWidget(label)
    return dialog

def build(build_dict: dict):
    # put up a display in the stdout
    print("""
    +-----------------------------+
    |                             |
    | Building the Configuration. |
    | Do not close the terminal!  |
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
        log("Build Failed: The error message shuold be displayed below.")
        log("Exiting to main menu...")
        return

    log("Build Succeeded. Adding Entry to Builds List...")

    # Add the new build entry to the builds list
    build_dict["playable"] = True
    build_dict["execPath"] = os.path.join(FOLDER_PATH, f"repo/build/{build_dict['romRegion']}_pc/sm64.{build_dict['romRegion']}.f3dex2e")

    # save the dict
    os.remove(os.path.join(FOLDER_PATH, "./build.json"))

    with open(os.path.join(FOLDER_PATH, "./build.json"), "w+") as buildjsonfile:
        buildjsonfile.write(parse_to_json(build_dict))
    
    # exit
    return 