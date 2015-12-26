"""
Use the default Python version and see what it is.

A change to the used python version can be made by changing the value of:
    Main Menu > Mods > Raspberry Jam Mod > Config > Python Interpreter
From:
    `python`
To:
    a fully qualified path to an alternate Python interpreter

Example from Mac OS with Python3 added via Homebrew:
    /usr/local/bin/python3
Example from Windows:
    C:\Python27\python.exe
"""

import sys

print(sys.version_info)
