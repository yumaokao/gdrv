#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import logging
import urllib2
import fnmatch
import colorama
import progressbar
from apiclient import errors
from command_list import CommandList

lg = logging.getLogger("DRIVE.TRASH")
# lg.setLevel(logging.INFO)


class CommandTrash(CommandList):
    """ A Drive Command Class """

    @staticmethod
    def static_add_sub_command_parser(psub_par):
        cmdparser = psub_par.add_parser('trash',
                                        help='command trash help')
        cmdparser.add_argument('src', nargs='+',
                               help='google drive files')

    def do_service_command(self):
        """trash files
        """

        # lg.debug(self.args)
        pulls = self.get_all_src_files(self.args.src, hidedir=False)

        if len(pulls) == 0:
            sys.exit("No files matched in drive")
        self.info(colorama.Fore.RED +
                  "Would you like to trash these files ?" +
                  colorama.Style.RESET_ALL)
        self.show_files_info(pulls, pnum=True)
        inpstr = self.choose_files(pulls)
        allidxs = self.parse_input_string(inpstr, len(pulls))
        for pidx in allidxs:
            self.trash_a_file(pulls[pidx])

# ## private methods ##
    def trash_a_file(self, pfile, pname=None):
        lg.debug("title %s id %s" % (pfile['title'], pfile['id']))
        try:
            self.service.files().trash(fileId=pfile['id']).execute()
        except errors.HttpError, error:
            lg.error('An error occured: %s' % error)
            return None
        self.info("file %s is trashed" % pfile['title'])
