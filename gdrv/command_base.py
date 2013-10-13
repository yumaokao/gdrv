#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import logging
import httplib2
import global_mod as gm
from apiclient.discovery import build
from oauth2client.file import Storage

lg = logging.getLogger("BASE")
#lg.setLevel(logging.INFO)


class DriveCommand():
    """ A Drive Command Class """

    def __init__(self, psub_par):
        self.subparser = psub_par
        self.init_cmdparser()

    def init_cmdparser(self):
        self.cmdparser = None

    def do_command(self, args=None):
        self.args = args
        self.do_drive_command()

    def do_drive_command(self):
        pass

    def info(self, *args):
        try:
            sys.stdout.write(*args)
            sys.stdout.write('\n')
        except UnicodeError:
            pass


class DriveServiceCommand(DriveCommand):
    """ A Drive Service Command Class """

    def get_storage(self):
        self.storage = Storage(
            os.path.expanduser(gm.config.get('api', 'storage')))

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

## helper drive apis ##
    def find_parent_id(self, pdir, pmkdir=False):
        dirs = pdir.split('/')
        parentid = 'root'
        #for aidx in range(len(dirs)):
        for adir in dirs:
            #lg.debug("dirs %s" % (adir))
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
        #lg.debug("query %s" % query)
        children_dirs = self.file_list(query)
        #for adir in children_dirs:
        #    lg.debug("children %s id %s" % (adir['title'], adir['id']))
        return children_dirs

## basic drive apis ##
    def file_list(self, query=""):
        """Retrieve a list of File resources.

        Args:
          service: Drive API service instance.
        Returns:
          List of File resources.
        """
        #lg.debug("file_list query %s" % query)
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
