#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import logging
import urllib2
import fnmatch
import colorama
import progressbar
import global_mod as gm
from apiclient import errors
from command_base import DriveServiceCommand

lg = logging.getLogger("PULL")
lg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(name)s] %(levelname)s - %(message)s')
ch.setFormatter(formatter)
lg.addHandler(ch)


class CommandPull(DriveServiceCommand):
    """ A Drive Command Class """

    def init_cmdparser(self):
        ## python2.7 lack of aliases of add_parser in sub command.
        self.cmdparser = self.subparser.add_parser('pull',
                                                   help='command list help')
        ### for query string composing ###
        self.cmdparser.add_argument('src', nargs='+',
                                    help='source files')
        self.cmdparser.add_argument('-O', '--output', nargs=1,
                                    help='desination')

    def do_service_command(self):
        """pull files
        """

        #lg.debug(self.args)
        pulls = []
        for asrc in self.args.src:
            dirname = os.path.dirname(asrc)
            basename = os.path.basename(asrc)
            ## TODO check basename is None
            lg.debug("src dirname %s basename %s" % (dirname, basename))
            files = self.find_src_files(dirname, basename)
            pulls.extend(files)

        if len(pulls) == 0:
            sys.exit("No files matched in drive")
        print(colorama.Fore.RED +
              "Would you like to pull these files ?" +
              colorama.Style.RESET_ALL)
        for pidx in range(len(pulls)):
            ## TODO colorama
            print "%d %s" % (pidx, pulls[pidx]['title'])
        inpstr = raw_input("[a]= all, [0-%d]: number: " %
                           (len(pulls) - 1)).strip()
        allidxs = self.parse_input_string(inpstr, len(pulls))
        for pidx in allidxs:
            self.pull_a_file(pulls[pidx])

## private methods ##
    def parse_input_string(self, pinstr, pmaxlen):
        idxs = []
        if pinstr == 'a':
            return range(pmaxlen)
        for acom in pinstr.split(','):
            arange = acom.split('-')
            #lg.debug("aidx ")
            #lg.debug(arange)
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
            #lg.debug("aidx %d bidx %d") % (aidx, bidx)
        #ridx = filter(lambda x: x < pmaxlen, idxs)
        #lg.debug(ridx)
        return set(filter(lambda x: x < pmaxlen, idxs))

    def pull_a_file(self, pfile):
        #lg.debug("title %s url %s" % (pfile['title'], pfile['downloadUrl']))
        try:
            auth = {}
            self.credentials.apply(auth)
            #lg.debug("auth header %s" % auth)
            req = urllib2.Request(pfile['downloadUrl'])
            for key, val in auth.iteritems():
                #lg.debug("auth header key %s val %s" % (key, val))
                req.add_header(key, val)
            res = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            lg.debug(e)
            sys.exit("%s: %s" % (pfile['title'], e))
        http_size = int(res.info().getheader('Content-Length').strip())
        drive_size = int(pfile['fileSize'])
        #lg.debug("size http %d drive %d" % (http_size, drive_size))

        print "%s downloading ..." % pfile['title']
        tmpfile = "%s.part" % pfile['title']
        size = http_size
        chunk_size = 1024 * 1024
        with open(tmpfile, 'w') as fout:
            pbar = progressbar.ProgressBar(
                widgets=[progressbar.Percentage(),
                         progressbar.Bar()],
                maxval=size).start()
            pull_size = 0
            buf = res.read(chunk_size)
            while buf != "":
                pull_size += len(buf)
                #lg.debug("%d of %d bytes downloaded" % (pull_size, http_size))
                pbar.update(pull_size)
                fout.write(buf)
                buf = res.read(chunk_size)
            pbar.finish()

        if pull_size != http_size:
            lg.warn("only %d of %d bytes downloaded, maybe incompleted" %
                    (pull_size, http_size))
        else:
            os.rename(tmpfile, pfile['title'])
            #print "%s download completed" % pfile['title']

    def get_all_children_files(self, psrcdir, pflat=False):
        ## TODO recursive
        parentid = self.find_parent_id(psrcdir)
        if parentid is None:
            lg.error("Can't find directory %s in drive" % psrcdir)
            sys.exit("Can't find directory %s in drive" % psrcdir)
        query = "'%s' in parents" % parentid
        query += " and mimeType != 'application/vnd.google-apps.folder'"
        query += " and trashed = false"
        return self.file_list(query)

    def find_src_files(self, psrcdir, pname):
        matches = []
        files = self.get_all_children_files(psrcdir)
        for afile in files:
            if fnmatch.fnmatch(afile['title'], pname):
                matches.append(afile)
        return matches
