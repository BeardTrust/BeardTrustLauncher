#!/usr/bin/env python3
import os
import signal
import subprocess

from scripts.process_management import operating_system

from argparse import Namespace

import scripts.process_management

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
    process = None

    if args.configuration.lower() == 'spring-boot':
        process = scripts.process_management.run_spring_boot_microservice(args.root_directory, args.profile)
    elif args.configuration.lower() == 'npm':
        process = scripts.process_management.run_npm_microservice(args.root_directory)
    elif args.configuration.lower() == 'yarn':
        process = scripts.process_management.run_yarn_microservice(args.root_directory)

    process_list.write(str(process.pid) + ',')
    process_list.close()


def close_applications():
    process_list = open(process_list_filename, 'r')
    processes = process_list.read().split(',')

    for pid in processes:
        try:
            if len(pid) > 0:
                process_details = subprocess.call('ps -A | grep ' + pid, shell=True)
                print(process_details)
                process = subprocess.Popen(pid)
                scripts.process_management.terminate_process(process)
        except ProcessLookupError:
            pass

    process_list.close()
    process_list = open(process_list_filename, 'w')
    process_list.close()
