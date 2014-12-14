#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import logging
import fnmatch
import httplib2
from apiclient import errors
from apiclient.discovery import build
from oauth2client.file import Storage

lg = logging.getLogger("BASE")
# lg.setLevel(logging.INFO)


class DriveCommand():
    """ A Drive Command Class """

    def __init__(self, pconfig):
        self.config = pconfig
        self.msgout = sys.stdout

    @staticmethod
    def static_add_sub_command_parser(psub_par):
        pass

    def __call__(self, args=None):
        if args is not None:
            self.args = args
        self.do_drive_command()

    def do_drive_command(self):
        pass

# ## base command methods ##
    def info(self, *args):
        try:
            self.msgout.write(*args)
            self.msgout.write('\n')
            self.msgout.flush()
        except UnicodeError:
            pass

    def info_append(self, *args):
        try:
            self.msgout.write(*args)
            self.msgout.flush()
            # self.msgout.write('\n')
        except UnicodeError:
            pass

    def parse_input_string(self, pinstr, pmaxlen):
        idxs = []
        if pinstr == 'a':
            return range(pmaxlen)
        for acom in pinstr.split(','):
            arange = acom.split('-')
            # lg.debug("aidx ")
            # lg.debug(arange)
            try:
                if len(arange) == 1:
                    aidx = int(arange[0])
                    idxs.append(aidx)
                elif len(arange) == 2:
                    aidx = int(arange[0])
                    bidx = int(arange[1])
                    idxs.extend(range(aidx, bidx + 1))
            except ValueError:
                pass
            # lg.debug("aidx %d bidx %d") % (aidx, bidx)
        # ridx = filter(lambda x: x < pmaxlen, idxs)
        # lg.debug(ridx)
        return set(filter(lambda x: x < pmaxlen, idxs))


class DriveServiceCommand(DriveCommand):
    """ A Drive Service Command Class """

    def get_storage(self):
        self.storage = Storage(
            os.path.expanduser(self.config.get('api', 'storage')))

    def get_credentials(self):
        self.credentials = None
        self.get_storage()
        self.credentials = self.storage.get()

    def get_service(self):
        self.service = None
        self.get_credentials()
        if self.credentials is None or self.credentials.invalid:
            print "Please init oauth2 flow first"
        else:
            http = httplib2.Http()
            http = self.credentials.authorize(http)
            self.service = build('drive', 'v2', http=http)

    def do_drive_command(self):
        self.get_service()
        if self.service is not None:
            self.do_service_command()

    def do_service_command(self):
        pass

# ## helper drive apis ##
    def find_drive_files(self, psrcdir, pname,
                         hidedir=False, hidetrashed=True):
        matches = []
        files = self.get_all_children(psrcdir,
                                      hidedir=hidedir, hidetrashed=hidetrashed)
        for afile in files:
            if fnmatch.fnmatch(afile['title'], pname):
                matches.append(afile)
        return matches

    def get_all_children(self, psrcdir, hidedir=False, hidetrashed=True):
        parentid = self.find_parent_id(psrcdir)
        if parentid is None:
            lg.error("Can't find directory %s in drive" % psrcdir)
            sys.exit("Can't find directory %s in drive" % psrcdir)
        query = "'%s' in parents" % parentid
        if hidedir is True:
            query += " and mimeType != 'application/vnd.google-apps.folder'"
        if hidetrashed is True:
            query += " and trashed = false"
        return self.file_list(query)

    def find_parent_id(self, pdir, pmkdir=False):
        dirs = pdir.split('/')
        parentid = 'root'
        # for aidx in range(len(dirs)):
        for adir in dirs:
            # lg.debug("dirs %s" % (adir))
            if adir == '':
                continue
            children_dirs = self.check_children_dirs(adir, parentid)
            dirs_nums = len(children_dirs)
            if dirs_nums == 0:
                lg.error("Can't find directory %s" % (adir))
                return None
            elif dirs_nums > 1:
                lg.warn("Find %d instances of directory %s" % (
                    dirs_nums, adir))
            parentid = children_dirs[0]['id']
        return parentid

    def check_children_dirs(self, dirname, parent="root"):
        query = "mimeType = 'application/vnd.google-apps.folder'"
        query += " and title = '%s'" % dirname
        query += " and '%s' in parents" % parent
        # lg.debug("query %s" % query)
        children_dirs = self.file_list(query)
        # for adir in children_dirs:
        #     lg.debug("children %s id %s" % (adir['title'], adir['id']))
        return children_dirs

# ## basic drive apis ##
    def file_list(self, query=""):
        """Retrieve a list of File resources.

        Args:
          service: Drive API service instance.
        Returns:
          List of File resources.
        """
        # lg.debug("file_list query %s" % query)
        result = []
        page_token = None
        while True:
            try:
                param = {}
                if query != "":
                    param['q'] = query
                if page_token:
                    param['pageToken'] = page_token
                files = self.service.files().list(**param).execute()

                result.extend(files['items'])
                page_token = files.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                break
        return result

    def permission_list(self, pfile="root"):
        """Retrieve a list of permissions of the file

        Args:
          pfile: drive file id
        Returns:
          list of file permissions
        """
        # lg.debug("permission_list query %s" % query)
        result = []
        page_token = None
        while True:
            try:
                param = {}
                if page_token:
                    param['pageToken'] = page_token
                perms = self.service.permissions().list(fileId=pfile).execute()

                result.extend(perms['items'])
                page_token = perms.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                break
        return result

    # deprecated
    def children_list(self, parent="root", query=""):
        """Retrieve a list of File resources.

        Args:
          parent: parent id or alias 'root'
          query: query string
        Returns:
          List of File resources.
        """
        result = []
        page_token = None
        while True:
            try:
                param = {}
                if query != "":
                    param['q'] = query
                if page_token:
                    param['pageToken'] = page_token
                files = self.service.children().list(
                    folderId=parent, **param).execute()

                result.extend(files['items'])
                page_token = files.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                break
        return result
