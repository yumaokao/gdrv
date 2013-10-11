#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import logging
import global_mod as gm
from apiclient import errors
from apiclient.http import MediaFileUpload
from command_base import DriveServiceCommand

lg = logging.getLogger("PUSH")
#lg.setLevel(logging.INFO)


class CommandPush(DriveServiceCommand):
    """ A Drive Command Class """

    def init_cmdparser(self):
        ## python2.7 lack of aliases of add_parser in sub command.
        self.cmdparser = self.subparser.add_parser('push',
                                                   help='command list help')
        ### for query string composing ###
        self.cmdparser.add_argument('src', nargs='+',
                                    help='source files')
        self.cmdparser.add_argument('dst', nargs=1,
                                    help='desination')

    def do_service_command(self):
        """push files
        """

        lg.debug("YMK in do_command")
        lg.debug(self.args)
        #sys.stderr.write("YMK STDERR\n")
        parentid = self.find_dst_dir()
        if parentid is None:
            lg.error("Can't find directory %s in drive" % self.args.dst[0])
            sys.exit("Can't find directory %s in drive" % self.args.dst[0])

        ## check src files exists in local
        for src in self.args.src:
            if os.path.exists(src):
                lg.debug("%s exists" % src)

        ## TODO check files exist in drive
        ## TODO to create or update

        for src in self.args.src:
            title = os.path.basename(src)
            #lg.debug("title %s put in %s" % (title, parentid))
            afile = self.file_insert(src, title, parentid)
            if afile is None or not afile['title'] == title:
                lg.error("File %s push error", src)
            else:
                lg.debug("File %s pushed in drive as id %s" % (
                    afile['title'], afile['id']))

## private methods ##
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
        ## TODO: add optioneal properties.
        #'description': description,
        #'mimeType': mime_type
        body = {
            'title': title
            }
        # Set the parent folder.
        if parent_id:
            body['parents'] = [{'id': parent_id}]

        try:
            file = self.service.files().insert(
                body=body,
                media_body=media_body).execute()
            return file
        except errors.HttpError, error:
            lg.error('An error occured: %s' % error)
            return None

    def find_dst_dir(self):
        dstdir = self.args.dst[0]
        return self.find_parent_id(dstdir)

## not used
    def get_children_dirs(self, parent="root"):
        query = "mimeType = 'application/vnd.google-apps.folder'"
        query += " and '%s' in parents" % parent
        #return self.children_list(parent, query)
        return self.file_list(query)

    def get_all_dirs(self):
        query = "mimeType = 'application/vnd.google-apps.folder'"
        return self.file_list(query)
