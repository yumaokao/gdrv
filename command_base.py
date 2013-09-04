#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import httplib2
import global_mod as gm
from apiclient.discovery import build
from oauth2client.file import Storage


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
