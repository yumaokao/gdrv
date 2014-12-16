#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

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

#   ### ymk ###
    def do_ymk(self, line):
        print("YMK FTP get_names() {0}".format(self.get_names()))

    def complete_ymk(self, text, line, begidx, endidx):
        return ["yumaokao", "yumao.kao", "yumaokao74", "ymk74"]

#   ### init ###
    def do_init(self, line):
        args = self.parser.parse_args()
        self.commands['init'](args)

#   ### cd ###
    def do_cd(self, line):
        print("YMK ls in {0}".format(self.pwd))
        self.pwd = line

    def complete_cd(self, text, line, begidx, endidx):
        return ["yumaokao", "yumao.kao", "yumaokao74", "ymk74"]

#   ### ls ###
    def do_ls(self, line):
        print("YMK ls in {0}".format(self.pwd))
        args = self.parser.parse_args(("list {0}".format(self.pwd)).split())
        print("YMK ls args {0}".format(args))
        self.commands['list'](args)

    def complete_ls(self, text, line, begidx, endidx):
        return ["yumaokao", "yumao.kao", "yumaokao74", "ymk74"]


# if __name__ == '__main__':
#    DriveFtp().cmdloop()
