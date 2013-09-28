#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import logging
import global_mod as gm
from apiclient import errors
from command_base import DriveServiceCommand

lg = logging.getLogger("PUSH")
lg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(name)s] %(levelname)s - %(message)s')
ch.setFormatter(formatter)
lg.addHandler(ch)


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
        sys.stderr.write("YMK STDERR\n")
        print "dst %s" % self.args.dst
        self.find_dst_dir()
        for src in self.args.src:
            if os.path.exists(src):
                print "%s exists" % src


## private methods ##
    def find_dst_dir(self):
        dstdir = self.args.dst[0]
        parents = False
        dirs = self.args.dst[0].split('/')
        print "dirs %s" % dirs


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
