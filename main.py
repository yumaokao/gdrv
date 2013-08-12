#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import sys
import argparse
import re
import logging
from command_list import CommandList


lg = logging.getLogger("DRIVE_MAIN")
lg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(name)s] %(levelname)s - %(message)s')
ch.setFormatter(formatter)
lg.addHandler(ch)


drive_commands = []
#drive_commands1 = [CommandList]


def main():
    global drive_commands

    lg.debug("YMK Goodbye World!!!")
    parser = argparse.ArgumentParser(
        description='YMK google drive command line tool')
    #parser.add_argument('command', nargs=1, choices=drive_commands)
    #parser.add_argument('others', nargs='?')
    subparser = parser.add_subparsers(help='drive sub command')

    drive_commands = [CommandList(subparser)]

    args = parser.parse_args()
    lg.debug(args)


if __name__ == '__main__':
    main()
