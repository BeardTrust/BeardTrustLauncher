#!/usr/bin/env python3
import os
import subprocess


def start_application(root_directory, profile):
    print("running 'mvn clean spring-boot:run -Dspring-boot.run.arguments=--spring.profiles.active=" + profile + "'" +
          " from " + root_directory)
    os.chdir(root_directory)
    subprocess.Popen('mvn clean spring-boot:run -Dspring-boot.run.arguments=--spring.profiles.active=' + profile,
                     shell=True)
