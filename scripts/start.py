#!/usr/bin/env python3

import os
import subprocess


def run_spring_boot_microservice(root_directory, profile):
    """
    This function directs a call to the host system to launch a Maven-based Spring Boot application
    using the specified profile.

    :param root_directory: str          the path to the application's root directory
    :param profile: str                 the Spring profile to set as active
    :return: process                    the newly launched process
    """

    print("running 'mvn clean spring-boot:run -Dspring-boot.run.arguments=--spring.profiles.active=" + profile + "'" +
          " from " + root_directory)
    os.chdir(root_directory)
    new_process = subprocess.Popen('mvn clean spring-boot:run -Dspring-boot.run.arguments=--spring.profiles.active=' +
                                   profile, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

    return new_process
