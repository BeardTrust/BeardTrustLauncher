#!/usr/bin/env python3
import subprocess
import platform
from os import chdir

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
    launch_command = ['npm', 'install', '&&', 'npm', 'start']

    output_launch_command(launch_command, root_directory)

    chdir(root_directory)

    return execute_command(launch_command)


def run_yarn_microservice(root_directory: str) -> subprocess.Popen:
    """
    This function directs a call to the host system to launch an application using Yarn.
    :param root_directory: str          the string representation of the path to the application's root directory
    :return: Popen                      the newly-created process
    """
    launch_command = ['yarn', 'install', '&&', 'yarn', 'start']

    output_launch_command(launch_command, root_directory)

    chdir(root_directory)

    return execute_command(launch_command)


def output_launch_command(launch_command: list[str], root_directory: str) -> None:
    print("[= BeardTrust Launcher =] Running '" + ' '.join(launch_command) + "' from '" + root_directory + "'")


def execute_command(launch_command: list[str]) -> subprocess.Popen:
    if platform.system().lower() == 'windows':
        process = subprocess.Popen(launch_command, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                                   shell=True)
    else:
        process = subprocess.Popen(launch_command, stdout=subprocess.DEVNULL)

    return process
