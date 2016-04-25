#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for whiteplanes executed. """
import io
import sys
import unittest
from whiteplanes import Whiteplanes


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


########################################################################
# Execute Test
########################################################################
class ExecuteTest(unittest.TestCase):

    def setUp(self):
        self.capture = io.StringIO()
        sys.stdout = self.capture

    def test_hello(self):
        with open('./test/etc/hello_world.ws') as f:
            code = f.read()
        interpreter = Whiteplanes(code)
        interpreter.run(context=Context())
        self.assertEqual('Hello World\n', self.capture.getvalue())

    def test_heapcontrol(self):
        with open('./test/etc/heap_control.ws') as f:
            code = f.read()
        interpreter = Whiteplanes(code)
        interpreter.run(context=Context())
        self.assertEqual('Hello World\n', self.capture.getvalue())

    def test_flow(self):
        with open('./test/etc/flow_control.ws') as f:
            code = f.read()
        interpreter = Whiteplanes(code)
        interpreter.run(context=Context())
        self.assertEqual('52', self.capture.getvalue())

    def test_count(self):
        with open('./test/etc/count.ws') as f:
            code = f.read()
        interpreter = Whiteplanes(code)
        interpreter.run(context=Context())
        self.assertEqual('1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n',
                         self.capture.getvalue())

    def test_input(self):
        with open('./test/etc/input.ws') as f:
            code = f.read()
        interpreter = Whiteplanes(code)
        interpreter.run(context=Context())
        self.assertEqual('H72', self.capture.getvalue())
