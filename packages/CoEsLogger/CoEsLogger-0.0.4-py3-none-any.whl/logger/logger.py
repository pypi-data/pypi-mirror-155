# -*- coding: utf-8 -*-

class Logger(object):

    def begin(self):
        pass

    def commit(self):
        pass

    def error(self, message,ex, **kwargs):
        pass

    def warn(self, message, **kwargs):
        pass

    def info(self, message, **kwargs):
        pass

    def debug(self, message, **kwargs):
        pass

