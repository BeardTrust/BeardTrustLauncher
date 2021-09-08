#!/usr/bin/env python3

import pkg_resources
import subprocess


def check_for_wxpython(mode):
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s" % package.key for package in installed_packages])

    if 'wxpython' not in installed_packages_list:
        if mode == 'gui':
            install_dependencies()
        else:
            print("[=Error=] Unable to locate wxPython.  Install now?\n")
            install_response = str(input("Install wxPython (y/N): "))

            if install_response.lower() == 'y' or install_response == 'yes':
                install_dependencies()


def install_dependencies():
    subprocess.run('pip install wxPython', shell=True)
