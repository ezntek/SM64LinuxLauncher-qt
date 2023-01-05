# Contributing

### Syntax Guidelines

* Follows PEP8 Syntax Guidelines
* **PLEASE PLEASE** annotate as many variables as possible with types
* Comments: explain **why** an element is there

### Project Outline

```
.
├── SM64LinuxLauncher-qt
│   ├── launcher
│   │   ├── build.py
│   │   ├── dialogs.py
│   │   ├── __main__.py
│   │   ├── res
│   │   │   ├── img
│   │   │   │   └── (Images and other assets go here)
│   │   │   ├── repos
│   │   │   │   └── repos.json
│   │   │   ├── sample_build.json
│   │   │   ├── ui
│   │   │   │   └── (Qt Designer Files go here)
│   │   │   └── version.json
│   │   └── uic
│   │       └── (Transpiled .ui files go here)
│   └── setup.py
└── tools
    ├── builduis.py
    └── make_release.py
```

There are 3 files with active human-written code:
* `build.py` for the compilation code AND build.json parser
* `__main__.py` the entry point of the app (contains QApplication, MainWindow)
* `dialogs.py` all the dialog classes go here

The tools folder contains the tools (ALL MUST BE RAN FROM THE ROOT OF THE REPOSITORY)
*  `builduis.py` will convert the `.ui` files to python classes (from `SM64LinuxLauncher-qt/launcher/res/ui/*` to `SM64LinuxLauncher-qt/launcher/uic/*`, run after saving a UI file)
* `make_release.py` will make a release tarball.

# Development Dependencies

* **A GNU/Linux environment**
* Qt Designer (5 or 6 are all okay)
* `git`
* `python3` (Version 3.10 and above)
    * `PyQt6` (with `pyuic6`)
    * `poetry`
    * `gitpython`
    * `requests` (for the `setup.py` script)
* `sdl2` with headers (for testing pcport builds)
* `glew` with headers (for testing pcport builds)
* a C Compiler (preferably `gcc`, for testing pcport builds)

### Distro-Specific Dependency Installation
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

`pip install --user gitpython PyQt6 requests`

# Running

Run `SM64LinuxLauncher-qt/launcher` within poetry.