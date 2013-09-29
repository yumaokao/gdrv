#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import logging
import global_mod as gm
from apiclient import errors
from command_base import DriveServiceCommand

lg = logging.getLogger("PULL")
lg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(name)s] %(levelname)s - %(message)s')
ch.setFormatter(formatter)
lg.addHandler(ch)


class CommandPull(DriveServiceCommand):
    """ A Drive Command Class """

    def init_cmdparser(self):
        ## python2.7 lack of aliases of add_parser in sub command.
        self.cmdparser = self.subparser.add_parser('pull',
                                                   help='command list help')
        ### for query string composing ###
        self.cmdparser.add_argument('src', nargs='+',
                                    help='source files')
        self.cmdparser.add_argument('-O', '--output', nargs=1,
                                    help='desination')

    def do_service_command(self):
        """pull files
        """

        lg.debug("YMK in do_command")
        lg.debug(self.args)
        #sys.stderr.write("YMK STDERR\n")
        #parentid = self.find_dst_dir()
        for asrc in self.args.src:
            dirname = os.path.dirname(asrc)
            basename = os.path.basename(asrc)
            ## TODO check basename is None
            lg.debug("src dirname %s basename %s" % (dirname, basename))
            files = self.find_src_files(dirname, basename)

## private methods ##
    def find_src_files(self, psrcdir, pname):
        parentid = self.find_parent_id(psrcdir)
        if parentid is None:
            lg.error("Can't find directory %s in drive" % psrcdir)
            sys.exit("Can't find directory %s in drive" % psrcdir)
