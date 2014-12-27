#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import logging
import urllib2
import fnmatch
import colorama
import progressbar
from apiclient import errors
# from command_base import DriveServiceCommand
from command_list import CommandList

lg = logging.getLogger("DRIVE.PULL")
# lg.setLevel(logging.INFO)


class CommandPull(CommandList):
    """ A Drive Command Class """

    @staticmethod
    def static_add_sub_command_parser(psub_par):
        cmdparser = psub_par.add_parser('pull',
                                        help='command pull help')
        cmdparser.add_argument('src', nargs='+',
                               help='google drive files')
        cmdparser.add_argument('-o', '--output', nargs=1,
                               help='desination')

    def do_service_command(self):
        """pull files
        """

        self.msgout = sys.stdout
        if self.args.output is not None:
            if self.args.output[0] == '-':
                self.msgout = sys.stderr

        # lg.debug(self.args)
        pulls = self.get_all_src_files(self.args.src, hidedir=True)

        if len(pulls) == 0:
            sys.exit("No files matched in drive")
        self.info(colorama.Fore.RED +
                  "Would you like to pull these files ?" +
                  colorama.Style.RESET_ALL)
        self.show_files_info(pulls, pnum=True)
        inpstr = self.choose_files(pulls)
        allidxs = self.parse_input_string(inpstr, len(pulls))
        if self.args.output is not None:
            if not len(allidxs) == 1:
                lg.error("Mutilple output filenames not yet supported")
            else:
                for pidx in allidxs:
                    self.pull_a_file(pulls[pidx], self.args.output[0])
        else:
            for pidx in allidxs:
                self.pull_a_file(pulls[pidx])

# ## private methods ##
    def pull_a_file(self, pfile, pname=None):
        # lg.debug("title %s url %s" % (pfile['title'], pfile['downloadUrl']))
        try:
            auth = {}
            self.credentials.apply(auth)
            # lg.debug("auth header %s" % auth)
            url = pfile.get('downloadUrl')
            if url is None:
                url = pfile['exportLinks']['application/pdf']

            req = urllib2.Request(url)
            for key, val in auth.iteritems():
                # lg.debug("auth header key %s val %s" % (key, val))
                req.add_header(key, val)
            res = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            lg.debug(e)
            sys.exit("%s: %s" % (pfile['title'], e))

        if res.info().getheader('Content-Length') is not None:
            http_size = int(res.info().getheader('Content-Length').strip())
        else:
            file_size = pfile.get('fileSize')
            http_size = 1024 * 1024 * 1024 if file_size is None else int(file_size)
        # drive_size = int(pfile['fileSize'])
        # lg.debug("size http %d drive %d" % (http_size, drive_size))

        self.info("%s downloading ..." % pfile['title'])
        if pname is None:
            tmpfile = "%s.part" % pfile['title']
        else:
            tmpfile = "%s.part" % pname
        size = http_size
        chunk_size = 1024 * 1024
        # with open(tmpfile, 'w') as fout:
        try:
            # lg.debug("[%s]" % pname)
            if pname is not None and pname == '-':
                fout = sys.stdout
            else:
                fout = open(tmpfile, 'w')
            pbar = progressbar.ProgressBar(
                widgets=[progressbar.Percentage(),
                         progressbar.Bar()],
                maxval=size).start()
            pull_size = 0
            buf = res.read(chunk_size)
            while buf != "":
                pull_size += len(buf)
                # lg.debug("%d of %d bytes downloaded" % (pull_size, http_size))
                pbar.update(pull_size)
                fout.write(buf)
                buf = res.read(chunk_size)
            pbar.finish()
        except IOError, e:
            if fout == sys.stdout:
                pass
            else:
                lg.error("IOError, %s" % e)
        finally:
            if not fout == sys.stdout:
                fout.close()

        if pull_size != http_size and http_size != 1024 * 1024 * 1024:
            lg.warn("only %d of %d bytes downloaded, maybe incompleted" %
                    (pull_size, http_size))
        else:
            if fout != sys.stdout:
                os.rename(tmpfile, pfile['title'])
            # print "%s download completed" % pfile['title']
