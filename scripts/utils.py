#!/usr/bin/env python3
import os
from subprocess import run

from pkg_resources import working_set


def check_for_wxpython(mode: str) -> None:
    """
    This function determines whether or not wxPython has been installed on the host system.  If
    wxPython is not found, this function will either prompt the user to install wxPython if the
    user is utilizing the command line interface, or will automatically install wxPython if the
    user is utilizing the graphical user interface.

    :param mode: str            the interface being utilized by the user (cli or gui)
    :return: None               this function does not return a value
    """
    installed_packages = working_set
    installed_packages_list = sorted(["%s" % package.key for package in installed_packages])

    if 'wxpython' not in installed_packages_list:
        if mode == 'gui':
            install_dependencies()
        else:
            print("[=Error=] Unable to locate wxPython.  Install now?\n")
            install_response = str(input("Install wxPython (y/N): "))

            if install_response.lower() == 'y' or install_response == 'yes':
                install_dependencies()


def install_dependencies() -> None:
    """
    This function runs the command to install wxPython on the host system.

    :return: None           this function does not return a value
    """
    run(['pip', 'install', 'wxPython'])


def get_local_group_service_paths(root_directory: str) -> dict[str, str]:
    services = {
        'accountservice': root_directory + '/AccountService',
        'adminportal': root_directory + '/AdminPortal',
        'cardservice': root_directory + '/CardService',
        'discoveryservice': root_directory + '/DiscoveryService',
        'gateway': root_directory + '/Gateway',
        'loanservice': root_directory + '/LoanService',
        'transactionservice': root_directory + '/TransactionService',
        'userportal': root_directory + '/UserPortal',
        'userservice': root_directory + '/UserService'
    }

    return services
