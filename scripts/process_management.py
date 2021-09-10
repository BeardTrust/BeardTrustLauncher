#!/usr/bin/env python3
import subprocess
import platform
from os import chdir

import scripts.utils

operating_system = platform.system().lower()

def run_spring_boot_microservice(root_directory: str, profile: str) -> subprocess.Popen:
    """
    This function directs a call to the host system to launch a Maven-based Spring Boot application
    using the specified profile.

    :param root_directory: str          the path to the application's root directory
    :param profile: str                 the Spring profile to set as active
    :return: process                    the newly-created Popen object
    """

    launch_command = ['mvn', 'clean', 'spring-boot:run', '-Dspring-boot.run.arguments=--spring.profiles.active=' +
                      profile]

    output_launch_command(launch_command, root_directory)

    chdir(root_directory)

    return execute_command(launch_command)


def run_npm_microservice(root_directory: str) -> subprocess.Popen:
    """
    This function directs a call to the host system to launch an application using NPM.
    :param root_directory: str          the string representation of the path to the application's root directory
    :return: Popen                      the newly-created process
    """
    launch_command = ['npm', 'start']

    output_launch_command(launch_command, root_directory)

    chdir(root_directory)

    return execute_command(launch_command)


def run_yarn_microservice(root_directory: str) -> subprocess.Popen:
    """
    This function directs a call to the host system to launch an application using Yarn.
    :param root_directory: str          the string representation of the path to the application's root directory
    :return: Popen                      the newly-created process
    """
    launch_command = ['yarn', 'start']

    output_launch_command(launch_command, root_directory)

    chdir(root_directory)

    return execute_command(launch_command)


def output_launch_command(launch_command: list[str], root_directory: str) -> None:
    print("[= BeardTrust Launcher =] Running '" + ' '.join(launch_command) + "' from '" + root_directory + "'")


def execute_command(launch_command: list[str]) -> subprocess.Popen:
    if operating_system == 'windows':
        process = subprocess.Popen(launch_command, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                                   shell=True)
    else:
        process = subprocess.Popen(launch_command, stdout=subprocess.DEVNULL)

    return process


def terminate_process(process: subprocess.Popen) -> int:
    return_value = 0

    if operating_system == 'windows':
        return_value = subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
    else:
        process.terminate()

    return return_value


def launch_all_applications(root_directory: str, profile: str) -> list[subprocess.Popen]:
    services = scripts.utils.get_local_group_service_paths(root_directory)

    processes = []

    for key in services.keys():
        chdir(services[key])

        if key == 'adminportal':
            processes.append(run_yarn_microservice(services[key]))
        elif key == 'userportal':
            processes.append(run_yarn_microservice(services[key]))
        else:
            processes.append(run_spring_boot_microservice(services[key], profile))

        chdir(root_directory)
    return processes
