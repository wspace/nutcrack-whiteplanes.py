#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from command import Command, Register


########################################################################
# Context
########################################################################
class Context(metaclass=ABCMeta):

    @abstractmethod
    def input(self, name):
        pass

    @abstractmethod
    def output(self, value):
        pass


########################################################################
# Whiteplanes
########################################################################
class Whiteplanes(object):
    def __init__(self, code):
        self.code = code
        self.commands = Whiteplanes.pause(code)

    def run(self, *, context=None):
        Context.register(type(context))
        [command(context=context) for command in self.commands if command.name == Register]

        while (context.counter < len(self.commands)):
            command = self.commands[context.counter]
            if command.name == Register:
                context.counter += 1
                continue
            command(context=context)
            context.counter += 1

    @classmethod
    def pause(cls, source):
        code = [ch for ch in source if ch in Command.characters()]
        return [command for command in Command.make(code)]
