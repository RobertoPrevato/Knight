import sys
from cx_Freeze import setup, Executable

# run like this:
#
# Linux:
# sudo python setup.py build
#
# Windows: (with right Python version inside the path)
# C:\Python34\python setup.py build
#
build_exe_options = {"packages": ["os", "core", "lib"] }

# NB: change executable to have the right path for you!
executablePath = "/home/ug/Projects/git/Knight/source/knight.py"

setup(
    name = "Knight",
    version = "1.0",
    description = "Angular and Knockout templates packer. Packs .html files into .js for Angular or Knockout.",
    options = {"build_exe": build_exe_options},
    executables = [Executable(executablePath)]
)
