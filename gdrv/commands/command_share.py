#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import fnmatch
import logging
from apiclient import errors
from command_base import DriveServiceCommand
from command_list import CommandList

lg = logging.getLogger("DRIVE.SHARE")
# lg.setLevel(logging.INFO)


class CommandShare(CommandList):
    """ A Drive Command Class """

    @staticmethod
    def static_add_sub_command_parser(psub_par):
        cmdparser = psub_par.add_parser('share',
                                        help='command share help')
        cmdparser.add_argument('src', nargs='+',
                               help='patterns to list in google drive')

        cmdparser.add_argument('-u', '--unshare', action='store_true',
                               help='unshare files')

    def do_service_command(self):
        """share files
        """

        lg.debug("YMK in do_command")
        lg.debug(self.args)

        files = self.get_all_src_files(self.args.src, False)

        if len(files) == 0:
            sys.exit("No files matched in drive")

        sfiles = []
        for pidx in range(len(files)):
            perms = self.permission_list(files[pidx]['id'])
            perms = filter(lambda p: p['type'] == 'anyone', perms)
            shared = 'shared' if len(perms) > 0 else ''

            if 'webContentLink' in files[pidx]:
                link = files[pidx]['webContentLink']
            elif 'alternateLink' in files[pidx]:
                link = files[pidx]['alternateLink']
            else:
                link = files[pidx]['id']

            sfiles.append({'idx': pidx, 'title': files[pidx]['title'], 'id': files[pidx]['id'],
                           'shared': shared, 'link': link})
            self.info("%2d %s \n  (%s)  %s" % (pidx, files[pidx]['title'], shared, link))

        inpstr = self.choose_files(sfiles)
        allidxs = self.parse_input_string(inpstr, len(sfiles))
        for aidx in allidxs:
            if self.args.unshare is True:
                if sfiles[aidx]['shared'] == 'shared':
                    self.info("unsharing %s" % sfiles[aidx]['title'])
                    self.unshare_a_file(sfiles[aidx]['id'])
            else:
                if sfiles[aidx]['shared'] == '':
                    self.info("sharing %s" % sfiles[aidx]['title'])
                    self.share_a_file(sfiles[aidx]['id'])

# ## private methods ##
    def share_a_file(self, pfid, pvalue=None, ptype='anyone', prole='reader'):
        nperm = {
            'value': pvalue,
            'type': ptype,
            'role': prole
        }
        try:
            return self.service.permissions().insert(fileId=pfid, body=nperm).execute()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None
        self.info("%s shared" % (pfid))

    def unshare_a_file(self, pfid, pvalue=None, ptype='anyone', prole='reader'):
        perms = self.permission_list(pfid)
        perms = filter(lambda p: p['type'] == 'anyone', perms)
        for aperm in perms:
            try:
                self.service.permissions().delete(
                    fileId=pfid, permissionId=aperm['id']).execute()
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                return None
        self.info("fid %s unshared" % (pfid))
