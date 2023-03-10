import subprocess
import os

if __name__ == "__main__":
    for ui in os.listdir('./SM64LinuxLauncher-qt/launcher/res/ui'):
        name, ext = os.path.splitext(ui)
        if ext == ".ui":
            subprocess.run(f"pyuic6 ./SM64LinuxLauncher-qt/launcher/res/ui/{ui} -o ./SM64LinuxLauncher-qt/launcher/uic/{name}_ui.py", shell=True)
            print(f"Converted {ui}")