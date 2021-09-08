#!/usr/bin/env python3
import os
import signal
import subprocess

from argparse import Namespace

import scripts.start

process_list_filename = '.beardtrust-processes.txt'


def command_line_interface(args: Namespace) -> None:
    """
    This function launches the specified Maven-based Spring Boot application via the command line interface.

    :param args: Namespace          the list of command line arguments
    :return: None               this function does not return a value
    """

    if args.quit == True:
        close_applications()
    else:
        launch_application(args)


def launch_application(args):
    process_list = open('.beardtrust-processes.txt', 'a')
    process = scripts.start.run_spring_boot_microservice(args.root_directory, args.profile)
    process_list.write(str(process.pid) + ',')
    process_list.close()


def close_applications():
    process_list = open(process_list_filename, 'r')
    processes = process_list.read().split(',')

    for process in processes:
        if len(process) > 0:
            os.kill(int(process), signal.SIGINT)

    process_list.close()
    process_list = open(process_list_filename, 'w')
    process_list.close()
