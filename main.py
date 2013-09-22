#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import os
import sys
import argparse
import re
import logging
import ConfigParser

import global_mod as gm
from command_list import CommandList
from command_init import CommandInit
from command_push import CommandPush


lg = logging.getLogger("DRIVE_MAIN")
lg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(name)s] %(levelname)s - %(message)s')
ch.setFormatter(formatter)
lg.addHandler(ch)


drive_commands = {}


def load_default_config():
    gm.config = ConfigParser.RawConfigParser()
    gm.config.add_section('api')
    gm.config.set('api', 'client_id',
                  '741789474926.apps.googleusercontent.com')
    gm.config.set('api', 'client_secret', 'ZZI0GSvLNLEHYUNsBsrmkG2y')
    gm.config.set('api', 'redirect_url', 'http://127.0.0.1')
    gm.config.set('api', 'scope', 'https://www.googleapis.com/auth/drive')
    gm.config.set('api', 'storage', '~/.drivegoogle/credentials.dat')


def get_config(args=None):
    load_default_config()

    ## YMK TODO: -f filename and -w filename
    lg.debug("YMK dump config api ")
    lg.debug(gm.config.items('api'))
    last_cfg_name = ""
    for cfg_path in gm.config_paths:
        cfg_name = os.path.expanduser(cfg_path + '.' + gm.app_name + 'rc')
        lg.debug("YMK config file check %s", cfg_name)
        if os.path.exists(cfg_name):
            last_cfg_name = cfg_name
            gm.config.read(cfg_name)

    if args.write_config is True:
        if last_cfg_name == "":
            new_cfg_name = os.path.expanduser(gm.config_paths[0] + '.' +
                                              gm.app_name + 'rc')
            lg.debug("YMK let's make a new one %s", new_cfg_name)
            with open(new_cfg_name, 'w+') as configfile:
                gm.config.write(configfile)


def main():
    global drive_commands

    lg.debug("YMK Goodbye World!!!")

    parser = argparse.ArgumentParser(
        description='YMK google drive command line tool')
    parser.add_argument('-w', '--write-config', action='store_true',
                        help='write a default config')
    subparser = parser.add_subparsers(help='drive sub command',
                                      dest='command_name')

    drive_commands = {'list': CommandList(subparser),
                      'push': CommandPush(subparser),
                      'init': CommandInit(subparser)}

    args = parser.parse_args()

    get_config(args)

    drive_commands[args.command_name].do_command(args)


if __name__ == '__main__':
    main()
