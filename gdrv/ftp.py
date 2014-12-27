#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

from os import getcwd, listdir, chdir
from os.path import isdir, join, isfile, split
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

# ################
#   ### REMOTE ###
# ################
#   ### pwd ###
    def do_pwd(self, line):
        print(Fore.BLUE + "GDRV PWD: {0}".format(self.pwd) + Style.RESET_ALL)

#   ### ls ###
    def do_ls(self, line):
        # print("YMK ls in {0}".format(self.pwd))
        # args = self.parser.parse_args(("list {0}".format(self.pwd)).split())
        # print("YMK ls args {0}".format(args))
        self.commands['list'].get_service()
        self.cache_inodes = self.commands['list'].get_all_src_files(self.pwd)
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
        print("YMK ls in {0}".format(self.pwd))
        self.pwd = line

    def complete_cd(self, text, line, begidx, endidx):
        return ["yumaokao", "yumao.kao", "yumaokao74", "ymk74"]

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
