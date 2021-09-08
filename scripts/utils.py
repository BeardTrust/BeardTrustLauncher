#!/usr/bin/env python3

import subprocess

import pkg_resources


def check_for_wxpython(mode):
    """
    This function determines whether or not wxPython has been installed on the host system.  If
    wxPython is not found, this function will either prompt the user to install wxPython if the
    user is utilizing the command line interface, or will automatically install wxPython if the
    user is utilizing the graphical user interface.

    :param mode: str            the interface being utilized by the user (cli or gui)
    :return: None               this function does not return a value
    """
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
    """
    This function runs the command to install wxPython on the host system.

    :return: None           this function does not return a value
    """
    subprocess.run('pip install wxPython', shell=True)
