#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai


class DriveCommand():
    """ A Drive Command Class """

    def __init__(self, psub_par):
        self.subparser = psub_par
        self.init_cmdparser()

    def init_cmdparser(self):
        self.cmdparser = None

    def do_command(self, args=None):
        self.args = args
        self.do_drive_command()

    def do_drive_command(self):
        pass


class DriveServiceCommand(DriveCommand):
    """ A Drive Service Command Class """

    def do_drive_command(self):
        self.do_service_command()

    def do_service_command(self):
        pass
