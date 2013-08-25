#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import logging
from command_base import DriveCommand

lg = logging.getLogger("INIT")
lg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(name)s] %(levelname)s - %(message)s')
ch.setFormatter(formatter)
lg.addHandler(ch)


class CommandInit(DriveCommand):
    """ A Drive Command Class """

    def init_cmdparser(self):
        ## python2.7 lack of aliases of add_parser in sub command.
        self.cmdparser = self.subparser.add_parser('init',
                                                   help='command list help')
        self.cmdparser.add_argument('queries', nargs='?',
                                    help='other query string for search files')
        self.cmdparser.add_argument('-m', '--max-results',
                                    type=int, default=100,
                                    help='maximum number of files to return')
        self.cmdparser.add_argument('-o', '--operator',
                                    choices=['and', 'or'], default='and',
                                    help='logical operator between query'
                                         'strings')

        ### for query string composing ###
        self.cmdparser.add_argument('-t', '--title', nargs='*',
                                    help='title of the file')
        self.cmdparser.add_argument('-f', '--full-text', nargs='*',
                                    help='full text of the file including'
                                         'title, description, and content')

    def do_command(self, args=None):
        lg.debug("YMK in do_command")
        lg.debug(args)
