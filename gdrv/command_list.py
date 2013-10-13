#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import fnmatch
import logging
import global_mod as gm
from apiclient import errors
from command_base import DriveServiceCommand

lg = logging.getLogger("DRIVE.LIST")
#lg.setLevel(logging.INFO)


class CommandList(DriveServiceCommand):
    """ A Drive Command Class """

    def init_cmdparser(self):
        ## python2.7 lack of aliases of add_parser in sub command.
        self.cmdparser = self.subparser.add_parser('list',
                                                   help='command list help')
        self.cmdparser.add_argument('pat', nargs='+',
                                    help='patterns to list in google drive')

    def do_service_command(self):
        """list files
        """

        lg.debug("YMK in do_command")
        lg.debug(self.args)

        pulls = []
        for asrc in self.args.pat:
            dirname = os.path.dirname(asrc)
            basename = os.path.basename(asrc)
            ## TODO check basename is None
            lg.debug("src dirname %s basename %s" % (dirname, basename))
            files = self.find_src_files(dirname, basename)
            pulls.extend(files)

        if len(pulls) == 0:
            sys.exit("No files matched in drive")

        for pidx in range(len(pulls)):
            self.info("%d %s" % (pidx, pulls[pidx]['title']))

## private methods ##
    def get_all_children(self, psrcdir, pflat=False):
        ## TODO recursive
        parentid = self.find_parent_id(psrcdir)
        if parentid is None:
            lg.error("Can't find directory %s in drive" % psrcdir)
            sys.exit("Can't find directory %s in drive" % psrcdir)
        query = "'%s' in parents" % parentid
        query += " and trashed = false"
        return self.file_list(query)

    def find_src_files(self, psrcdir, pname):
        matches = []
        files = self.get_all_children(psrcdir)
        for afile in files:
            if fnmatch.fnmatch(afile['title'], pname):
                matches.append(afile)
        return matches
