#!/usr/bin/env python3
import requests
import shutil
import stat
import os

def log(string: str):
    return f"LOG: {string}"

def setup() -> None:
    release_url = "https://github.com/tek967/SM64LinuxLauncher-qt/releases/download/v0.1.0/release.tar.gz"

    # download the tarball
    print(f"LOG: downloading from {release_url}...")
    with open('./sm64linuxlauncher-qt.tar.gz', "wb") as tarball:
        tarball.write(requests.get(release_url).content)
    
    # decompress the tarball
    print("LOG: decompressing archive...")
    shutil.unpack_archive("./sm64linuxlauncher-qt.tar.gz", "./", "gztar")

    # rename the folder
    shutil.move("./dist", os.path.join(os.environ['HOME'],"SM64LinuxLauncher-qt"))

    # make __main__.py executable
    print("LOG: making the program executable...")
    mainpy = os.stat(os.path.join(os.environ['HOME'], "./SM64LinuxLauncher-qt/__main__.py"))
    os.chmod(os.path.join(os.environ['HOME'], "./SM64LinuxLauncher-qt/__main__.py"), mainpy.st_mode | stat.S_IEXEC)

    # clean up
    print("LOG: tidyinp up...")
    os.remove("./sm64linuxlauncher-qt.tar.gz")

    print("The setup process is now complete. Refer to the online manual for further instructions.")


# Driver Code
if __name__ == "__main__":
    setup()