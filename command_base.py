#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai


class DriveCommand():
    """ A Drive Command Class """

    def __init__(self, psub_par):
        self.subparser = psub_par
        self.init_cmdparser()

    def init_cmdparser(self):
        self.cmdparser = None

    def do_command(self):
        pass
