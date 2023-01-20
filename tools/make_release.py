import os
import shutil
import json
import sys

def main():
    SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    # copy the launcher folder
    shutil.copytree(os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/launcher"), os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/dist"))

    # remove some debug related and noncritical files
    shutil.rmtree(os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/dist/res/ui"))
    shutil.rmtree(os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/dist/uic/__pycache__"))
    shutil.rmtree(os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/dist/__pycache__"))
    shutil.rmtree(os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/dist/builds"))
    os.remove(os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/dist/res/sample_build.json"))

    try:
        match sys.argv[1]:
            case "--gz":
                # compress the directory
                shutil.make_archive("release", "gztar", "./SM64LinuxLauncher-qt/", "dist", verbose=True)

                # delete the folder
                shutil.rmtree(os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/dist"))
            case "--dir":
                with open(os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/launcher/res/version.json")) as versionjson:
                    d: dict = json.loads(versionjson.read())
                    shutil.copytree(os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/dist"), f"./release-{d['versionMajor']}.{d['versionMinor']}.{d['versionPatch']}")
                shutil.rmtree(os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/dist"))    
    except IndexError:
        # compress the directory
        shutil.make_archive("release", "gztar", "./SM64LinuxLauncher-qt/", "dist", verbose=True)

        # delete the folder
        shutil.rmtree(os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/dist"))
if __name__ == "__main__":
    main()