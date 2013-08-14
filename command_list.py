#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import logging
from command_base import DriveCommand

lg = logging.getLogger("LIST")
lg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(name)s] %(levelname)s - %(message)s')
ch.setFormatter(formatter)
lg.addHandler(ch)


class CommandList(DriveCommand):
    """ A Drive Command Class """

    def init_cmdparser(self):
        self.cmdparser = self.subparser.add_parser('list',
                                                   help='command list help')
        self.cmdparser.add_argument('help', nargs='?')
        self.cmdparser.add_argument('-q', '--query',
                                    help='filter by query string')

    def do_command(self):
        lg.debug("YMK in do_command")
