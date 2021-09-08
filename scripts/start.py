#!/usr/bin/env python3

import os
import subprocess


def run_spring_boot_microservice(root_directory, profile):
    """
    This function directs a call to the host system to launch a Maven-based Spring Boot application
    using the specified profile.

    :param root_directory: str          the path to the application's root directory
    :param profile: str                 the Spring profile to set as active
    :return: None                       this function does not return a value
    """

    print("running 'mvn clean spring-boot:run -Dspring-boot.run.arguments=--spring.profiles.active=" + profile + "'" +
          " from " + root_directory)
    os.chdir(root_directory)
    subprocess.Popen('mvn clean spring-boot:run -Dspring-boot.run.arguments=--spring.profiles.active=' + profile,
                     shell=True)
