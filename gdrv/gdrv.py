#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import argparse
from gdrv.commands import *


def main():
    parser = argparse.ArgumentParser(
        description='google drive command line tool')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='increse verbosity/logging level')

    args = parser.parse_args()
    # test = DriveCommand()

    print("YMK")

if __name__ == '__main__':
    main()
