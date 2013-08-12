#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import sys
import argparse
import re
import logging


lg = logging.getLogger("DRIVE_MAIN")
lg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(name)s] %(levelname)s - %(message)s')
ch.setFormatter(formatter)
lg.addHandler(ch)


drive_commands = ['info', 'list']


def command_list():
    lg.debug("YMK command_list!!!")
    parser = argparse.ArgumentParser(
        description='YMK google drive command line tool -- list')
    parser.add_argument('list', nargs='+')
    parser.add_argument('-q', '--query', help='filter with query string.')
    args = parser.parse_args()
    if args.list[0] != 'list':
        print parser.print_help()
    if len(args.list) > 1 and args.list[1] == 'help':
        print parser.print_help()

    lg.debug(args)


def main():
    lg.debug("YMK Goodbye World!!!")
    parser = argparse.ArgumentParser(
        description='YMK google drive command line tool')
    parser.add_argument('command', nargs=1, choices=drive_commands)
    parser.add_argument('others', nargs='?')
    args = parser.parse_args()

    lg.debug(args.command)
    if args.command[0] == 'list':
        command_list()


if __name__ == '__main__':
    main()
