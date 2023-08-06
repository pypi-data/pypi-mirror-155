# -*- coding: utf-8 -*-
#!python3


import os
import sys
a = sys.platform
def install():
    exitcode=os.system('python3 -m pip install pyinstaller')
    if exitcode == 0:
        exit(0)
    else:
        raise
def convert(file_path):
    exitcode=os.system('pyinstaller --onefile "{}"'.format(file_path))
    if exitcode == 0:
        os.system('rm -rf build')
        if a == 'win32':
            os.system('copy dist\\{}.exe .\\{}.exe'.format(file_path.split('\\')[-1].split(".")[0], file_path.split('\\')[-1].split(".")[0]))
        elif a=="darwin":
            os.system('cp ./dist/{} ./{}'.format(file_path.split('/')[-1].split(".")[0], file_path.split('/')[-1].split(".")[0]))
        elif a=="linux":
            os.system('cp dist/{} ./{}'.format(file_path.split('/')[-1].split(".")[0], file_path.split('/')[-1].split(".")[0]))
        os.system('rm -rf dist')
    else:
        raise
def main():
    if len(sys.argv)==1:
        print("Usage: python3 main.py convert <file>")
        print("Usage: python3 main.py install")
        raise
    if sys.argv[-1] == "install":
        install()
    elif sys.argv[-2] == "convert":
        convert(sys.argv[-1])
    else:
        print("Usage: python3 main.py convert <file>")
        print("Usage: python3 main.py install")
        raise
if __name__ == "__main__":
    main()


