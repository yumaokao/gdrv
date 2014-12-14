#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

from cmd import Cmd


class DriveFtp(Cmd):
    """ Google drive interactive mode """

    def __init__(self, commands, config):
        self.commands = commands
        self.config = config
        Cmd.__init__(self)

    def do_ymk(self, line):
        print("YMK FTP")

    def do_exit(self, line):
        return True

    def do_EOF(self, line):
        return True


# if __name__ == '__main__':
#    DriveFtp().cmdloop()
