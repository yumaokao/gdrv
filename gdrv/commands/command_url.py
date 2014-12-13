#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import fnmatch
import logging
from gdrv import global_mod as gm
from apiclient import errors
from command_base import DriveServiceCommand
from command_list import CommandList

lg = logging.getLogger("DRIVE.URL")
# lg.setLevel(logging.INFO)


class CommandUrl(CommandList):
    """ A Drive Command Class """

    def init_cmdparser(self):
        # ## python2.7 lack of aliases of add_parser in sub command.
        self.cmdparser = self.subparser.add_parser('url',
                                                   help='command url help')
        self.cmdparser.add_argument('src', nargs='+',
                                    help='patterns to list in google drive')

        self.cmdparser.add_argument('-a', '--altlink', action='store_true',
                                    help='show alternateLink to redirect google drive file information page')

    def do_service_command(self):
        """url files
        """

        lg.debug("YMK in do_command")
        lg.debug(self.args)

        files = self.get_all_src_files(self.args.src, False)

        if len(files) == 0:
            sys.exit("No files matched in drive")

        for pidx in range(len(files)):
            perms = self.permission_list(files[pidx]['id'])
            perms = filter(lambda p: p['type'] == 'anyone', perms)
            shared = 'shared' if len(perms) > 0 else ''
            # lg.debug("shared ? %s" % shared)
            # for aperm in perms:
            #     lg.debug("a perm kind %s type %s role %s" % (aperm['kind'], aperm['type'], aperm['role']))

            # TODO list display
            if 'webContentLink' in files[pidx] and not self.args.altlink:
                link = files[pidx]['webContentLink']
                # self.info("%d %s wcl %s" % (pidx, files[pidx]['title'], files[pidx]['webContentLink']))
            elif 'alternateLink' in files[pidx]:
                link = files[pidx]['alternateLink']
                # self.info("%d %s atl %s" % (pidx, files[pidx]['title'], files[pidx]['alternateLink']))
            else:
                link = files[pidx]['id']
                # self.info("%d %s id %s" % (pidx, files[pidx]['title'], files[pidx]['id']))

            self.info("%2d %s \n  (%s)  %s" % (pidx, files[pidx]['title'], shared, link))


# ## private methods ##
