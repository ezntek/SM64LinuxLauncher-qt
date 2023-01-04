import os
import shutil

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

    # compress the directory
    shutil.make_archive("release", "gztar", "./SM64LinuxLauncher-qt/", "dist", verbose=True)

    # delete the folder
    shutil.rmtree(os.path.join(SCRIPT_PATH, "../SM64LinuxLauncher-qt/dist"))

if __name__ == "__main__":
    main()