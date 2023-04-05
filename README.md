# SM64LinuxLauncher-qt

A rewrite of [SM64LinuxLauncher](https://github.com/Bloxxel64/SM64LinuxLauncher) in `PyQt6` with minimal dependencies.

# IMPORTANT NOTE!

This project is really a prototype for an actual, more advanced builder with an API in Rust. It is in the works [here](https://github.com/ezntek/smbuilder). This project is now deprecated, try to not use it.

### **This project aims to:**
* Bring more frequent changes and updates to the tool
* Allow for better distribution
* Bring More support for more GNU/Linux Distributions
* Improve desktop integration by using a native Linux toolkit (Qt)
* Bring Better Ease-Of-Use
* Bring more functionality
* Bring More modularity
* Allow the tool to be more extensible and more approachable by beginner Free Software/"Open Source" Software developers.

### **Currently Working on**:
* UI Refresh
* `build.json` handling

### **Project TODO**:
- [ ] DynOS pack support
- [ ] OTA Update System
- [ ] Intelligent detection for support of certain features
- [x] allow users view build.jsons
- [ ] allow users to edit build.jsons and rebuild from new edits
- [ ] make it less stand-out-ish against other system programs 
- [ ] add more graphics
- [x] Refresh the UI (new one already planned)
- [ ] `.desktop` files
- [ ] Put on PyPI / AUR / Gentoo Overlay / PPA

### [Contributing](CONTRIBUTING.md)

### **License**:
This project is licensed under the [GNU GPL Version 3](https://www.gnu.org/licenses/gpl-3.0.html) and Above License.

### **Installation**:
#### **Arch GNU/Linux and derivatives**
Install all dependencies (Can skip pip dependencies):

`# pacman -S base-devel python python-pip python-gitpython python-pyqt6 sdl2 glew`

#### **Debian GNU/Linux and derivatives**
`# apt install build-essential git python3 libglew-dev libsdl2-dev`


#### **Fedora GNU/Linux**
`# dnf install make gcc python3 glew-devel SDL2-devel`

#### **Void GNU/Linux**
`# xbps-install -S base-devel python3 SDL2-devel glew-devel`

### `pip` Dependency Installation

`pip install --user gitpython PyQt6`

### Download

The following command installs SM64LinuxLauncher-qt into your home folder.

`python3 -c "$(curl -fsSL https://raw.githubusercontent.com/tek967/SM64LinuxLauncher-qt/master/SM64LinuxLauncher-qt/setup.py)"`

Now the installation process should be complete. Navigate to your home directory, open the SM64LinuxLauncher-qt folder, and double-click on `__main__.py` to get started
