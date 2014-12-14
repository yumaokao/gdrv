#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import fnmatch
import logging
from colorama import Fore, Style
from apiclient import errors
from command_base import DriveServiceCommand

lg = logging.getLogger("DRIVE.LIST")
# lg.setLevel(logging.INFO)


class CommandList(DriveServiceCommand):
    """ A Drive Command Class """

    @staticmethod
    def static_add_sub_command_parser(psub_par):
        cmdparser = psub_par.add_parser('list',
                                        help='command list help')
        cmdparser.add_argument('src', nargs='+',
                               help='patterns to list in google drive')

    def do_service_command(self):
        """list files
        """

        lg.debug("YMK in do_command")
        lg.debug(self.args)

        files = self.get_all_src_files(self.args.src)

        if len(files) == 0:
            sys.exit("No files matched in drive")

        self.show_files_info(files)
        # for pidx in range(len(files)):
        #     if 'weViewLink' in files[pidx]:
        #         self.info("%d %s %s" % (pidx, files[pidx]['title'], files[pidx]['webViewLink']))
        #     elif 'webContentLink' in files[pidx]:
        #         self.info("%d %s %s" % (pidx, files[pidx]['title'], files[pidx]['webContentLink']))
        #     else:
        #         self.info("%d %s %s %s" % (pidx, files[pidx]['title'], files[pidx]['id'], files[pidx]['ownerNames'][0]))

# ## private methods ##
    def get_all_src_files(self, psrc, hidedir=False):
        allfiles = []
        for asrc in psrc:
            dirname = os.path.dirname(asrc)
            basename = os.path.basename(asrc)
            if basename == "":
                basename = '*'
            lg.debug("src dirname %s basename %s" % (dirname, basename))
            files = self.find_drive_files(dirname, basename, hidedir=hidedir)
            allfiles.extend(files)
        return allfiles

    def show_files_info(self, pfiles, pnum=False, plong=False):
        # if pnum is False:
        #     if plong is False:
        #         for apf in pfiles:
        #             self.info()

        if plong is False:
            for pidx in range(len(pfiles)):
                apf = pfiles[pidx]
                self.info_append(Fore.GREEN +
                                 "%s" % ("%2d " % pidx if pnum is True else "") +
                                 Style.RESET_ALL)
                self.info("%s" % (Fore.BLUE + apf['title'] + Style.RESET_ALL
                                  if apf['mimeType'] == 'application/vnd.google-apps.folder'
                                  else apf['title']))

    def choose_files(self, pfiles):
        self.info(Fore.GREEN +
                  "[a]= all, [0-%d]: number: " % (len(pfiles) - 1) +
                  Style.RESET_ALL)
        return raw_input().strip()
