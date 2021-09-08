#!/usr/bin/env python3

import argparse

import scripts.utils

parser = argparse.ArgumentParser(description='Process command line arguments to determine which service to launch')
parser.add_argument('--root-directory', '-r', dest='root_directory', default='',
                    help="specify the project's root directory")
parser.add_argument('--install', '-i', dest='install', help="install dependencies for " +
                    "BeardTrust Launcher", action="store_true")
args = parser.parse_args()


def launch_cli(arguments):
    from ui.cli import command_line_interface
    command_line_interface(arguments)


def launch_gui():
    from ui.gui import graphical_user_interface
    graphical_user_interface()


def main(arguments):
    """
    This is the primary function of the BeardTrust Launcher application.  It instantiates the GUI and handles the
    main application loop.

    :param arguments: the list of arguments passed via the command line when the application is run
    :return: None
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
