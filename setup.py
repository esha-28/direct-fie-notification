import sys
from cx_Freeze import setup, Executable


setup(name='File Information',version='1.0',
      description='created for demo',
      executables=[Executable("notification.py",
                              icon='iconfinder_Folder-Info_60178.ico',
                              shortcutDir="DesktopFolder")])
