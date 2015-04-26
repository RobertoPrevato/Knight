import sys
from cx_Freeze import setup, Executable

# run like this:
#
# Linux:
# sudo python setup.py build
#
# Windows: (with right Python version)
# C:\Python34\python.exe setup.py build
#
build_exe_options = {"packages": ["core", "lib"] }

# NB: change executable to have the right path for you!
executablePath = "/home/ug/Projects/git/Knight/source/knight.py"

base = None
if sys.platform == "win32":
	base = "Win32GUI"

setup(
	name = "Knight",
	version = "1.0",
	description = "Angular and Knockout templates packer. Packs .html files into .js for Angular or Knockout.",
	options = {"build_exe": build_exe_options},
	executables = [Executable(executablePath, base=base)]
)
