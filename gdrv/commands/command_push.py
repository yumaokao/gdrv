#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import logging
import progressbar
from apiclient import errors
from apiclient.http import MediaFileUpload
from command_base import DriveServiceCommand

lg = logging.getLogger("DRIVE.PUSH")
# lg.setLevel(logging.INFO)


class CommandPush(DriveServiceCommand):
    """ A Drive Command Class """

    @staticmethod
    def static_add_sub_command_parser(psub_par):
        cmdparser = psub_par.add_parser('push',
                                        help='command push help')
        # ### for query string composing ###
        cmdparser.add_argument('src', nargs='+',
                               help='source files')
        cmdparser.add_argument('dst', nargs=1,
                               help='desination')
        cmdparser.add_argument('-p', '--prarents', nargs=1,
                               help='no error if existing,'
                               'make parent directories as needed')

    def do_service_command(self):
        """push files
        """

        lg.debug("YMK in do_command")
        lg.debug(self.args)
        # sys.stderr.write("YMK STDERR\n")

        if len(self.args.src) > 1:
            if os.path.basename(self.args.dst[0]) != "":
                lg.error("Multiple source should put in a directory")
                sys.exit("Multiple source should put in a directory")
        else:
            title = os.path.basename(self.args.dst[0])

        parentid = self.find_dst_dir()
        if parentid is None:
            lg.error("Can't find directory %s in drive" % self.args.dst[0])
            sys.exit("Can't find directory %s in drive" % self.args.dst[0])

        # ## check src files exists in local
        for src in self.args.src:
            if not os.path.exists(src):
                lg.error("%s dosen't exists" % src)
                sys.exit("%s dosen't exists" % src)

        # ## TODO check files exist in drive
        # ## TODO to create or update

        for src in self.args.src:
            if title == "":
                title = os.path.basename(src)
            lg.debug("src %s title %s put in %s" % (src, title, parentid))
            afile = self.file_insert(src, title, parentid)
            if afile is None or not afile['title'] == title:
                lg.error("File %s push error", src)
            else:
                lg.debug("File %s pushed in drive as id %s" % (
                    afile['title'], afile['id']))

# ## private methods ##
    def file_insert(self, filename, title, parent_id):
        """Insert new file.

        Args:
            title: Title of the file to insert, including the extension.
            parent_id: Parent folder's ID.
            filename: Filename of the file to insert.
        Returns:
            Inserted file metadata if successful, None otherwise.
        """

        media_body = MediaFileUpload(filename, resumable=True)
        # ## TODO: add optioneal properties.
        # 'description': description,
        # 'mimeType': mime_type
        body = {
            'title': title
        }
        # Set the parent folder.
        if parent_id:
            body['parents'] = [{'id': parent_id}]

        try:
            req = self.service.files().insert(
                body=body,
                media_body=media_body)
            self.info("%s uploading ..." % title)
            pbar = progressbar.ProgressBar(
                widgets=[progressbar.Percentage(),
                         progressbar.Bar()],
                maxval=100).start()
            res = None
            while res is None:
                status, res = req.next_chunk()
                if status:
                    # lg.debug("%d%% uploaded", int(status.progress() * 100))
                    pbar.update(int(status.progress() * 100))
            return res
        except errors.HttpError, error:
            lg.error('An error occured: %s' % error)
            return None

    def find_dst_dir(self):
        dstdir = os.path.dirname(self.args.dst[0])
        return self.find_parent_id(dstdir)

# ## not used
    def get_children_dirs(self, parent="root"):
        query = "mimeType = 'application/vnd.google-apps.folder'"
        query += " and '%s' in parents" % parent
        # return self.children_list(parent, query)
        return self.file_list(query)

    def get_all_dirs(self):
        query = "mimeType = 'application/vnd.google-apps.folder'"
        return self.file_list(query)
