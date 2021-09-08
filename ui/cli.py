#!/usr/bin/env python3

import os
import subprocess

def command_line_interface(args):
    print("running 'mvn clean spring-boot:run -Dspring-boot.run.arguments=--spring.profiles.active=dev'" +
          " from args.root_directory")
    os.chdir(args.root_directory)
    subprocess.call('mvn clean spring-boot:run -Dspring-boot.run.arguments=--spring.profiles.active=dev', shell=True)