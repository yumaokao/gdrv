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
        #sys.stderr.write("YMK STDERR\n")
        parentid = self.find_dst_dir()
        for src in self.args.src:
            if os.path.exists(src):
                lg.debug("%s exists" % src)
        dirs = self.args.dst[0].split('/')
        title = dirs[-1]
        if title == "":
            title = os.path.basename(src)
        lg.debug("title %s put in %s" % (title, parentid))
        ## TODO check file exists

## private methods ##
    def find_dst_dir(self):
        dstdir = self.args.dst[0]
        parents = False
        dirs = self.args.dst[0].split('/')

        parentid = 'root'
        for aidx in range(len(dirs) - 1):
            lg.debug("dirs[%d] %s" % (aidx, dirs[aidx]))
            if aidx == 0 and dirs[0] == '':
                continue
            children_dirs = self.check_children_dirs(dirs[aidx], parentid)
            dirs_nums = len(children_dirs)
            if dirs_nums == 0:
                lg.debug("I can't find the dir %s" % (dirs[aidx]))
            elif dirs_nums > 1:
                lg.warn("I find %d %s" % (dirs_nums, dirs[aidx]))
            parentid = children_dirs[0]['id']
        return parentid

    def check_children_dirs(self, dirname, parent="root"):
        query = "mimeType = 'application/vnd.google-apps.folder'"
        query += " and title = '%s'" % dirname
        query += " and '%s' in parents" % parent
        lg.debug("query %s" % query)
        children_dirs = self.file_list(query)
        #for adir in children_dirs:
        #    lg.debug("children %s id %s" % (adir['title'], adir['id']))
        return children_dirs

    def get_children_dirs(self, parent="root"):
        query += " and '%s' in parents" % parent
        #return self.children_list(parent, query)
        return self.file_list(query)

        query = "mimeType = 'application/vnd.google-apps.folder'"

    def get_all_dirs(self):
        query = "mimeType = 'application/vnd.google-apps.folder'"
        return self.file_list(query)
