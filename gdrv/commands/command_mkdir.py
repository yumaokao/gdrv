#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import logging
import progressbar
from apiclient import errors
from apiclient.http import MediaFileUpload
from command_base import DriveServiceCommand

lg = logging.getLogger("DRIVE.MKDIR")
# lg.setLevel(logging.INFO)


class CommandMkdir(DriveServiceCommand):
    """ A Drive Command Class """

    @staticmethod
    def static_add_sub_command_parser(psub_par):
        cmdparser = psub_par.add_parser('mkdir',
                                        help='command mkdir help')
        # ## for query string composing ###
        cmdparser.add_argument('dst', nargs=1,
                               help='desination')
        cmdparser.add_argument('-p', '--prarents', nargs=1,
                               help='no error if existing,'
                               'make parent directories as needed')

    def do_service_command(self):
        """mkdir directory
        """

        lg.debug("YMK in do_command")
        lg.debug(self.args)
        # sys.stderr.write("YMK STDERR\n")

        newdir = os.path.split(self.args.dst[0])
        if newdir[1] == "":
            newdir = os.path.split(newdir[0])

        if newdir[1] == "":
            lg.error("Can't find directory %s" % newdir[1])
            sys.exit("Can't find directory %s" % newdir[1])

        parentid = self.find_dst_dir(newdir[0])
        if parentid is None:
            lg.error("Can't find directory %s in drive" % self.args.dst[0])
            sys.exit("Can't find directory %s in drive" % self.args.dst[0])

        dirid = self.dir_insert(newdir[1], parentid)

# ## private methods ##
    def dir_insert(self, dirname, parent_id):
        """Insert new directory.

        Args:
            parent_id: Parent folder's ID.
            dirname: name of the directory to insert.
        Returns:
            Inserted directory metadata if successful, None otherwise.
        """

        body = {
            'title': dirname,
            'mimeType': 'application/vnd.google-apps.folder',
            }
        # Set the parent folder.
        if parent_id:
            body['parents'] = [{'id': parent_id}]

        try:
            ndir = self.service.files().insert(
                body=body).execute()
            return ndir
        except errors.HttpError, error:
            lg.error('An error occured: %s' % error)
            return None

    def find_dst_dir(self, dstdir=None):
        if dstdir is None:
            dstdir = os.path.dirname(self.args.dst[0])
        return self.find_parent_id(dstdir)
