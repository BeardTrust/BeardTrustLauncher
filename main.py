#!/usr/bin/env python3

import argparse
import os
import subprocess

import wx

import ui.ui

parser = argparse.ArgumentParser(description='Process command line arguments to determine which service to launch')
parser.add_argument('--root-directory', '-r', dest='root_directory', help="specify the project's root directory")

args = parser.parse_args()

def main(arguments):

    app = wx.App()
    page = ui.ui.main_page(None)
    page.Show()
    app.MainLoop()
    # print("running 'mvn clean spring-boot:run -Dspring-boot.run.arguments=--spring.profiles.active=dev'" +
    #       " from args.root_directory")
    # os.chdir(args.root_directory)
    # subprocess.call('mvn clean spring-boot:run -Dspring-boot.run.arguments=--spring.profiles.active=dev', shell=True)


if __name__ == '__main__':
    main(args)
