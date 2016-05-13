#!/usr/bin/env python
# -*- coding: utf-8 -*-


########################################################################
# Context
########################################################################
class Context(object):

    def __init__(self):
        self.stack, self.heap, self.labels, self.callstack = [], {}, {}, []
        self.counter = 0

    def input(self, name):
        return 72 if name == "IIN" else 'H'

    def output(self, value):
        print(value, end='')