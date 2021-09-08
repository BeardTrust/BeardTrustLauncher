#!/usr/bin/env python3

import scripts.start


def command_line_interface(args):
    """
    This function launches the specified Maven-based Spring Boot application via the command line interface.

    :param args: str[]          the list of command line arguments
    :return: None               this function does not return a value
    """
    scripts.start.run_spring_boot_microservice(args)
