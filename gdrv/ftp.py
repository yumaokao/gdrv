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

    def __init__(self, commands, config):
        self.commands = commands
        self.config = config
        Cmd.__init__(self)
        setattr(self, 'do_gdrv', real_do_gdrv)
        setattr(self, 'complete_gdrv', real_complete_gdrv)

#    def completedefault(self, text, line, begidx, endidx):
#        return ["ymk", "exit", "gdrv"]

    def get_names(self):
        return dir(self)
#        return ["do_ymk", "do_exit", "do_gdrv", "do_help"]

    def do_ymk(self, line):
        print("YMK FTP get_names() {0}".format(self.get_names()))

    def complete_ymk(self, text, line, begidx, endidx):
        return ["yumaokao", "yumao.kao", "yumaokao74", "ymk74"]

    def do_exit(self, line):
        return True

    def do_EOF(self, line):
        return True


# if __name__ == '__main__':
#    DriveFtp().cmdloop()
