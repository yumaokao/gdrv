#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import logging
import webbrowser
import httplib2
from command_base import DriveServiceCommand

from apiclient import errors
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

lg = logging.getLogger("DRIVE.INIT")
# lg.setLevel(logging.INFO)


class CommandInit(DriveServiceCommand):
    """ A Drive Command Class """

    @staticmethod
    def static_add_sub_command_parser(psub_par):
        # ## python2.7 lack of aliases of add_parser in sub command.
        cmdparser = psub_par.add_parser('init',
                                        help='command init help')
        cmdparser.add_argument('queries', nargs='?',
                               help='other query string for search files')
        cmdparser.add_argument('-m', '--max-results',
                               type=int, default=100,
                               help='maximum number of files to return')
        cmdparser.add_argument('-o', '--operator',
                               choices=['and', 'or'], default='and',
                               help='logical operator between query'
                               'strings')

        # ## for query string composing ## #
        cmdparser.add_argument('-t', '--title', nargs='*',
                               help='title of the file')
        cmdparser.add_argument('-f', '--full-text', nargs='*',
                               help='full text of the file including'
                               'title, description, and content')

    def do_drive_command(self):
        lg.debug("YMK in do_command")
        lg.debug(self.args)
        lg.debug("YMK dump config api ")
        lg.debug(self.config.items('api'))
        scopes = "https://docs.google.com/feeds"

        flow = OAuth2WebServerFlow(client_id=self.config.get('api', 'client_id'),
                                   client_secret=self.config.get('api', 'client_secret'),
                                   scope=scopes,
                                   redirect_uri="http://127.0.0.1")

        self.get_credentials()
        if self.credentials is None or self.credentials.invalid:
            flow_info = flow.step1_get_device_and_user_codes()
            webbrowser.open_new_tab(flow_info.verification_url)
            print("Enter verrification code in url {0}: {1}".format(flow_info.verification_url, flow_info.user_code))
            raw_input("Then press any key to continue...".format(flow_info.user_code))
            self.credentials = flow.step2_exchange(device_flow_info=flow_info)
            if self.credentials:
                filename = os.path.expanduser(self.config.get('api', 'storage'))
                dirname = os.path.dirname(filename)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                self.storage.put(self.credentials)

        self.get_service()
        if self.service is not None:
            self.do_service_command()

    def do_service_command(self):
        self.print_about(self.service)

# ## private methods ##
    def print_about(self, service):
        """Print information about the user along with the Drive API settings.

        Args:
          service: Drive API service instance.
        """
        try:
            about = service.about().get().execute()

            print 'Current user name: %s' % about['name']
            print 'Root folder ID: %s' % about['rootFolderId']
            print 'Total quota (bytes): %s' % about['quotaBytesTotal']
            print 'Used quota (bytes): %s' % about['quotaBytesUsed']
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
