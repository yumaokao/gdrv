#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

from os import getcwd, listdir, chdir
from os.path import isabs, isdir, isfile, join, split, normpath, basename
from colorama import Fore, Style
from cmd import Cmd


def real_do_gdrv(line):
    print("YMK do_gdrv")


def real_complete_gdrv(text, line, begidx, endidx):
    return ["yumaokao", "yumao.kao", "yumaokao74", "ymk74"]


class DriveFtp(Cmd):
    """ Google drive interactive mode """

    prompt = 'gdrv> '

    def __init__(self, commands, config, parser):
        self.commands = commands
        self.config = config
        self.parser = parser
        self.pwd = '/'
        self.parentid = 'root'
        # YMK: local should be fast enough
        # self.cache_lpwd = getcwd()
        # self.cache_files = None
        # self.cache_dirs = None
        Cmd.__init__(self)
        # YMK: don't think this is a good idea, though it's cool.
#        setattr(self, 'do_gdrv', real_do_gdrv)
#        setattr(self, 'complete_gdrv', real_complete_gdrv)

    def get_names(self):
        return dir(self)

    def do_exit(self, line):
        return True

    def do_EOF(self, line):
        return True

#   ### init ###
    def do_init(self, line):
        args = self.parser.parse_args()
        self.commands['init'](args)

# ##################
#   ### TRANSFOR ###
# ##################
#   ### pull ###
    def do_pull(self, line):
        # print(Fore.BLUE + "GDRV PULL: {0}".format(line) + Style.RESET_ALL)
        inodes = filter(lambda i:
                        i['title'] == line and
                        i['mimeType'] != 'application/vnd.google-apps.folder',
                        self.cache_inodes)
        if len(inodes) == 1:
            # print("url {0}".format(inodes[0]))
            self.commands['pull'].get_service()
            self.commands['pull'].pull_a_file(inodes[0])
        else:
            print("No such file or directory")

    def complete_pull(self, text, line, begidx, endidx):
        return filter(lambda i: i.startswith(text), self.cache_files)

#   ### push ###
    def do_push(self, line):
        # print(Fore.BLUE + "GDRV PUSH: {0}".format(line) + Style.RESET_ALL)
        lfile = join(getcwd(), line)
        if isfile(lfile):
            self.commands['push'].get_service()
            self.commands['push'].file_insert(lfile, basename(lfile), self.parentid)
        else:
            print("No such file or directory")

    def complete_push(self, text, line, begidx, endidx):
        cwd = getcwd()
        bname = text
        if text.endswith('..'):
            return [text + '/']
        if len(line.split()) > 1:
            (dname, bname) = split(line.split()[1])
            newdir = join(getcwd(), dname)
            # print("newdir {0}".format(newdir))
            if isdir(newdir):
                cwd = newdir
        inodes = filter(lambda i: i.startswith(bname), listdir(cwd))
        return inodes

# ################
#   ### REMOTE ###
# ################
#   ### pwd ###
    def do_pwd(self, line):
        print(Fore.BLUE + "GDRV PWD: {0}".format(self.pwd) + Style.RESET_ALL)

#   ### ls ###
    def do_ls(self, line):
        # print("YMK ls in {0} parentid {1}".format(self.pwd, self.parentid))
        # args = self.parser.parse_args(("list {0}".format(self.pwd)).split())
        # print("YMK ls args {0}".format(args))
        self.commands['list'].get_service()
        self.cache_inodes = self.commands['list'].get_all_children(self.pwd)
        self.cache_dirs = filter(lambda i:
                                 i['mimeType'] == 'application/vnd.google-apps.folder',
                                 self.cache_inodes)
        self.cache_dirs = map(lambda d: d['title'], self.cache_dirs)
        self.cache_files = filter(lambda i:
                                  i['mimeType'] != 'application/vnd.google-apps.folder',
                                  self.cache_inodes)
        self.cache_files = map(lambda d: d['title'], self.cache_files)
        # print("YMK ls cache inodes {0}".format(self.cache_inodes))
        # print("YMK ls cache dirs {0}".format(self.cache_dirs))
        # self.commands['list'](args)
        for d in sorted(self.cache_dirs):
            print(Fore.BLUE + d + Style.RESET_ALL)
        for f in sorted(self.cache_files):
            print(f)

#   ### cd ###
    def do_cd(self, line):
        # print("YMK ls in {0}".format(self.pwd))
        self.commands['list'].get_service()
        newpwd = line if isabs(line) else normpath(join(self.pwd, line))
        dirn = newpwd if newpwd.endswith('/') else newpwd + '/'
        parentid = self.commands['list'].find_parent_id(dirn)
        if parentid is not None:
            self.pwd = newpwd
            self.parentid = parentid

    def complete_cd(self, text, line, begidx, endidx):
        if text.endswith('..'):
            return [text + '/']
        return filter(lambda i: i.startswith(text), self.cache_dirs)

#   ### mkdir ###
    def do_mkdir(self, line):
        # print("YMK ls in {0}".format(self.pwd))
        self.commands['mkdir'].get_service()
        ndir = self.commands['mkdir'].dir_insert(line, self.parentid)
        if ndir is None:
            print("Could not new directory '{0}'", line)

    def complete_mkdir(self, text, line, begidx, endidx):
        return (filter(lambda i: i.startswith(text), self.cache_dirs)
                + filter(lambda i: i.startswith(text), self.cache_files))

#   ### trash ###
    def do_trash(self, line):
        # print(Fore.BLUE + "GDRV TRASH: {0}".format(line) + Style.RESET_ALL)
        inodes = filter(lambda i: i['title'] == line, self.cache_inodes)
        if len(inodes) == 1:
            # print("url {0}".format(inodes[0]))
            self.commands['trash'].get_service()
            self.commands['trash'].trash_a_file(inodes[0])
        else:
            print("No such file or directory")

    def complete_trash(self, text, line, begidx, endidx):
        return (filter(lambda i: i.startswith(text), self.cache_dirs)
                + filter(lambda i: i.startswith(text), self.cache_files))

#   ### url ###
    def do_url(self, line):
        self.commands['url'].get_service()
        pwd = self.pwd + '/' if not self.pwd.endswith('/') else self.pwd
        pline = pwd if line == "" else line
        if pline.endswith('/'):
            inodes = self.commands['url'].get_all_src_files(pline.split(), False)
        else:
            inodes = filter(lambda i: i['title'] == pline, self.cache_inodes)

        if len(inodes) == 0:
            print("No files matched in drive")
        else:
            self.commands['url'].url_files(inodes)

    def complete_url(self, text, line, begidx, endidx):
        return (filter(lambda i: i.startswith(text), self.cache_dirs)
                + filter(lambda i: i.startswith(text), self.cache_files))

#   ### share ###
    def do_share(self, line):
        # pline = self.pwd if line == "" else line
        # pline = pline if pline.endswith('/') else pline + '/'
        self.commands['share'].get_service()
        files = filter(lambda i: i['title'] == line, self.cache_inodes)
        # files = self.commands['share'].get_all_src_files(pline.split(), False)
        if len(files) == 0:
            print("No files matched in drive")
        else:
            for afile in files:
                perms = self.commands['share'].permission_list(afile['id'])
                perms = filter(lambda p: p['type'] == 'anyone', perms)
                shared = 'shared' if len(perms) > 0 else ''
                # print(" file {0} id {1} share [{2}]".format(afile['title'], afile['id'], shared))
                if not shared:
                    self.commands['share'].share_a_file(afile['id'])
                    print("shared {0}".format(afile['title']))
                else:
                    self.commands['share'].unshare_a_file(afile['id'])
                    print("unshared {0}".format(afile['title']))

    def complete_share(self, text, line, begidx, endidx):
        return (filter(lambda i: i.startswith(text), self.cache_dirs)
                + filter(lambda i: i.startswith(text), self.cache_files))

# ###############
#   ### LOCAL ###
# ###############
#   ### lpwd ###
    def do_lpwd(self, line):
        print(Fore.BLUE + "CWD: {0}".format(getcwd()) + Style.RESET_ALL)

#   ### lls ###
    def do_lls(self, line):
        inodes = listdir(getcwd())
        dirs = filter(lambda i: isdir(i), inodes)
        files = filter(lambda i: isfile(i), inodes)

        dirs = filter(lambda d: not d.startswith('.'), dirs)
        files = filter(lambda d: not d.startswith('.'), files)
        for d in dirs:
            print(Fore.BLUE + d + Style.RESET_ALL)
        for f in files:
            print(f)
        # print("{0}".format(files))

#   ### lcd ###
    def do_lcd(self, line):
        if isdir(line):
            chdir(line)
        self.cache_lpwd = getcwd()
        self.do_lpwd(None)

    def complete_lcd(self, text, line, begidx, endidx):
        # YMK cmd can't hanle '/' well with text ?
        cwd = getcwd()
        bname = text
        if text.endswith('..'):
            return [text + '/']
        if len(line.split()) > 1:
            (dname, bname) = split(line.split()[1])
            newdir = join(getcwd(), dname)
            # print("newdir {0}".format(newdir))
            if isdir(newdir):
                cwd = newdir
        # print("cwd {0}".format(cwd))
        # print("listdir {0}".format(listdir(cwd)))
        dirs = filter(lambda i: isdir(join(cwd, i)), listdir(cwd))
        dirs = filter(lambda i: i.startswith(bname), dirs)
        return dirs

# if __name__ == '__main__':
#    DriveFtp().cmdloop()
