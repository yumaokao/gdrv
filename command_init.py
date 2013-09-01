#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import logging
import webbrowser
import global_mod as gm
from command_base import DriveCommand

from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

lg = logging.getLogger("INIT")
lg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(name)s] %(levelname)s - %(message)s')
ch.setFormatter(formatter)
lg.addHandler(ch)


class CommandInit(DriveCommand):
    """ A Drive Command Class """

    def init_cmdparser(self):
        ## python2.7 lack of aliases of add_parser in sub command.
        self.cmdparser = self.subparser.add_parser('init',
                                                   help='command list help')
        self.cmdparser.add_argument('queries', nargs='?',
                                    help='other query string for search files')
        self.cmdparser.add_argument('-m', '--max-results',
                                    type=int, default=100,
                                    help='maximum number of files to return')
        self.cmdparser.add_argument('-o', '--operator',
                                    choices=['and', 'or'], default='and',
                                    help='logical operator between query'
                                         'strings')

        ### for query string composing ###
        self.cmdparser.add_argument('-t', '--title', nargs='*',
                                    help='title of the file')
        self.cmdparser.add_argument('-f', '--full-text', nargs='*',
                                    help='full text of the file including'
                                         'title, description, and content')

    def do_command(self, args=None):
        lg.debug("YMK in do_command")
        lg.debug(args)
        lg.debug("YMK dump config api ")
        lg.debug(gm.config.items('api'))

        flow = OAuth2WebServerFlow(gm.config.get('api', 'client_id'),
                                   gm.config.get('api', 'client_secret'),
                                   gm.config.get('api', 'scope'),
                                   "http://127.0.0.1")
        storage = Storage(gm.config.get('api', 'storage'))
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            auth_uri = flow.step1_get_authorize_url()
            print "Please goto this link: [%s]" % auth_uri
            webbrowser.open_new_tab(auth_uri)
            ## YMK TODO: a http web page with clipbaord js for easy copy
            code = raw_input("Enter verrification code: ").strip()
            credentials = flow.step2_exchange(code)
            if credentials:
                storage.put(credentials)
