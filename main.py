#!/usr/bin/env python3

from argparse import ArgumentParser
from argparse import Namespace

import scripts.utils

parser = ArgumentParser(description='Process command line arguments to determine which service to launch')
parser.add_argument('--root-directory', '-r', dest='root_directory', default='',
                    help="specify the project's root directory")
parser.add_argument('--install', '-i', dest='install', help="install dependencies for " +
                                                            "BeardTrust Launcher", action="store_true")
args = parser.parse_args()


def launch_cli(arguments: Namespace) -> None:
    """
    This function handles launching the command line interface.

    :param arguments: str[]     the list of command line arguments
    :return: None               this function does not return a value
    """
    from ui.cli import command_line_interface
    command_line_interface(arguments)


def launch_gui() -> None:
    """
    This function handles launching the graphical user interface.

    :return: None               this function does not return a value
    """
    from ui.gui import graphical_user_interface
    graphical_user_interface()


def main(arguments: Namespace) -> None:
    """
    This is the primary function of the BeardTrust Launcher application.  It directs control to the appropriate
    module.

    :param arguments: str[]             the list of arguments passed via the command line when the application is run
    :return: None                       this function does not return a value
    """
    if arguments.install:
        scripts.utils.check_for_wxpython('cli')
    elif len(arguments.root_directory) > 0:
        launch_cli(arguments)
    else:
        scripts.utils.check_for_wxpython('gui')
        launch_gui()


if __name__ == '__main__':
    main(args)
