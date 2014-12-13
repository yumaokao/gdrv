#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import logging
import global_mod as gm
from apiclient import errors
from command_base import DriveServiceCommand

lg = logging.getLogger("DRIVE.SEARCH")
#lg.setLevel(logging.INFO)


class CommandSearch(DriveServiceCommand):
    """ A Drive Command Class """

    def init_cmdparser(self):
        ## python2.7 lack of aliases of add_parser in sub command.
        self.cmdparser = self.subparser.add_parser('search',
                                                   help='command search help')
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

    def do_service_command(self):
        """list files
        """

        lg.debug("YMK in do_command")
        lg.debug(self.args)

        files = self.retrieve_files()
        for fl in files:
            print fl
            #print "%s, %s, %s" % (fl['title'], fl['id'], fl['mimeType'])

## private methods ##
    def retrieve_files(self, query=""):
        """Retrieve a list of File resources.

        Args:
          service: Drive API service instance.
        Returns:
          List of File resources.
        """
        result = []
        page_token = None
        while True:
            try:
                param = {}
                if query != "":
                    param['q'] = "title contains '%s'" % (query)
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
