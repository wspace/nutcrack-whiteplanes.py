#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from enum import Enum


########################################################################
# Command
########################################################################
class Command(object):

    ####################################################################
    # Token
    ####################################################################
    class Token(Enum):
        PUSH = "  "
        COPY = " \t "
        SLIDE = " \t\n"
        DUPLICATE = " \n "
        SWAP = " \n\t"
        DISCARD = " \n\n"
        ADD = "\t   "
        SUB = "\t  \t"
        MUL = "\t  \n"
        DIV = "\t \t "
        MOD = "\t \t\t"
        STORE = "\t\t "
        RETRIEVE = "\t\t\t"
        REGISTER = "\n  "
        CALL = "\n \t"
        JUMP = "\n \n"
        EQUAL = "\n\t "
        LESS = "\n\t\t"
        RETURN = "\n\t\n"
        END = "\n\n\n"
        COUT = "\t\n  "
        IOUT = "\t\n \t"
        CIN = "\t\n\t "
        IIN = "\t\n\t\t"

        def __call__(self, *, context=None, parameter=None):
            cls = self.__class__
            if self == cls.PUSH:
                self.push(context=context, parameter=parameter)
            elif self == cls.COPY:
                self.copy(context=context, parameter=parameter)
            elif self == cls.SLIDE:
                self.slide(context=context, parameter=parameter)
            elif self == cls.DUPLICATE:
                self.duplicate(context=context)
            elif self == cls.SWAP:
                self.swap(context=context)
            elif self == cls.DISCARD:
                self.discard(context=context)
            elif self == cls.ADD:
                self.add(context=context)
            elif self == cls.SUB:
                self.sub(context=context)
            elif self == cls.MUL:
                self.mul(context=context)
            elif self == cls.DIV:
                self.div(context=context)
            elif self == cls.MOD:
                self.mod(context=context)
            elif self == cls.STORE:
                self.store(context=context)
            elif self == cls.RETRIEVE:
                self.retrieve(context=context)
            elif self == cls.REGISTER:
                self.register(context=context, parameter=parameter)
            elif self == cls.CALL:
                self.call(context=context, parameter=parameter)
            elif self == cls.JUMP:
                self.jump(context=context, parameter=parameter)
            elif self == cls.EQUAL:
                self.equal(context=context, parameter=parameter)
            elif self == cls.LESS:
                self.less(context=context, parameter=parameter)
            elif self == cls.RETURN:
                self.back(context=context)
            elif self == cls.END:
                self.end(context=context)
            elif self == cls.COUT:
                self.cout(context=context)
            elif self == cls.IOUT:
                self.iout(context=context)
            elif self == cls.CIN:
                self.cin(context=context)
            elif self == cls.IIN:
                self.iin(context=context)

        ######################################################################
        # Instruction
        ######################################################################

        def push(self, *, context=None, parameter=None):
            """ Evaluate the PUSH command. """
            context.stack.append(parameter['value'])

        def copy(self, *, context=None, parameter=None):
            """ Evaluate the COPY command. """
            context.stack.append(context.stack[parameter['value']])

        def slide(self, *, context=None, parameter=None):
            """ Evaluate the SLIDE command. """
            value = context.stack.pop()
            for index in range(0, parameter['value']):
                context.stack.pop()
            context.stack.append(value)

        def duplicate(self, *, context=None):
            """ Evaluate the DUPLICATE command. """
            context.stack.append(context.stack[-1])

        def swap(self, *, context=None):
            """ Evaluate the SWAP command. """
            c = context
            c.stack[-1], c.stack[-2] = c.stack[-2], c.stack[-1]

        def discard(self, *, context=None):
            """ Evaluate the DISCARD command. """
            context.stack.pop()

        def add(self, *, context=None):
            """ Evaluate the ADD command. """
            lhs, rhs = context.stack.pop(), context.stack.pop()
            context.stack.append(lhs + rhs)

        def sub(self, *, context=None):
            """ Evaluate the SUB command. """
            lhs, rhs = context.stack.pop(), context.stack.pop()
            context.stack.append(lhs - rhs)

        def mul(self, *, context=None):
            """ Evaluate the MUL command. """
            lhs, rhs = context.stack.pop(), context.stack.pop()
            context.stack.append(lhs * rhs)

        def div(self, *, context=None):
            """ Evaluate the DIV command. """
            lhs, rhs = context.stack.pop(), context.stack.pop()
            context.stack.append(lhs / rhs)

        def mod(self, *, context=None):
            """ Evaluate the MOD command. """
            lhs, rhs = context.stack.pop(), context.stack.pop()
            context.stack.append(lhs % rhs)

        def store(self, *, context=None):
            """ Evaluate the STORE command. """
            value, address = context.stack.pop(), context.stack.pop()
            context.heap[address] = value

        def retrieve(self, *, context=None):
            """ Evaluate the RETRIEVE command. """
            address = context.stack.pop()
            context.stack.append(context.heap[address])

        def register(self, *, context=None, parameter=None):
            """ Evaluate the REGISTER command. """
            context.labels[parameter['name']] = parameter['location']

        def call(self, *, context=None, parameter=None):
            """ Evaluate the CALL command. """
            context.callstack.append(parameter['location'])
            context.counter = context.labels[parameter['name']]

        def jump(self, *, context=None, parameter=None):
            """ Evaluate the JUMP command. """
            context.counter = context.labels[parameter['name']]

        def equal(self, *, context=None, parameter=None):
            """ Evaluate the TEST[EQUAL] command. """
            if context.stack.pop() == 0:
                context.counter = context.labels[parameter['name']]

        def less(self, *, context=None, parameter=None):
            """ Evaluate the TEST[LESS] command. """
            if context.stack.pop() < 0:
                context.counter = context.labels[parameter['name']]

        def back(self, *, context=None):
            """ Evaluate the RETURN command. """
            context.counter = context.callstack.pop()

        def end(self, *, context=None):
            """ Evaluate the END command. """
            context.counter = sys.maxsize - 1

        def cout(self, *, context=None):
            """ Evaluate the OUTPUT[CHARACTER] command. """
            value = context.stack.pop()
            context.output(chr(value))

        def iout(self, *, context=None):
            """ Evaluate the OUTPUT[INT] command. """
            value = context.stack.pop()
            context.output(value)

        def cin(self, *, context=None):
            """ Evaluate the INPUT[CHARACTER] command. """
            address = context.stack.pop()
            value = context.input("CIN")
            context.heap[address] = ord(value)

        def iin(self, *, context=None):
            """ Evaluate the INPUT[INT] command. """
            address = context.stack.pop()
            value = context.input("IIN")
            context.heap[address] = value

    def __init__(self, name, *, parameter=None):
        self.name = name
        self.parameter = parameter

    def __call__(self, *, context=None):
        self.name(context=context, parameter=self.parameter)

    @classmethod
    def make(cls, code):
        def parameter(index):
            param = ""
            for character in code[index:]:
                if character == " ":
                    param += "0"
                elif character == "\t":
                    param += "1"
                elif character == "\n":
                    return (param, len(param) + 1)

        cur, commands, count = 0, 0, len(code)
        while cur < count:
            token = code[cur:] if ((cur + 3) - count) >= 0 else code[cur:cur + 4]
            if "".join(token[0:2]) == cls.Token.PUSH.value:
                param, index = parameter(cur)
                cur += index
                yield Command(cls.Token.PUSH, parameter={'value': int(param, 2)})
            elif "".join(token[0:3]) == cls.Token.COPY.value:
                cur += 3
                param, index = parameter(cur)
                cur += index
                yield Command(cls.Token.COPY, parameter={'value': int(param, 2)})
            elif "".join(token[0:3]) == cls.Token.SLIDE.value:
                cur += 3
                param, index = parameter(cur)
                cur += index
                yield Command(cls.Token.SLIDE, parameter={'value': int(param, 2)})
            elif "".join(token[0:3]) == cls.Token.DUPLICATE.value:
                cur += 3
                yield Command(cls.Token.DUPLICATE)
            elif "".join(token[0:3]) == cls.Token.SWAP.value:
                cur += 3
                yield Command(cls.Token.SWAP)
            elif "".join(token[0:3]) == cls.Token.DISCARD.value:
                cur += 3
                yield Command(cls.Token.DISCARD)
            elif "".join(token[0:4]) == cls.Token.ADD.value:
                cur += 4
                yield Command(cls.Token.ADD)
            elif "".join(token[0:4]) == cls.Token.SUB.value:
                cur += 4
                yield Command(cls.Token.SUB)
            elif "".join(token[0:4]) == cls.Token.MUL.value:
                cur += 4
                yield Command(cls.Token.MUL)
            elif "".join(token[0:4]) == cls.Token.DIV.value:
                cur += 4
                yield Command(cls.Token.DIV)
            elif "".join(token[0:4]) == cls.Token.MOD.value:
                cur += 4
                yield Command(cls.Token.MOD)
            elif "".join(token[0:3]) == cls.Token.STORE.value:
                cur += 3
                yield Command(cls.Token.STORE)
            elif "".join(token[0:3]) == cls.Token.RETRIEVE.value:
                cur += 3
                yield Command(cls.Token.RETRIEVE)
            elif "".join(token[0:3]) == cls.Token.REGISTER.value:
                cur += 3
                param, index = parameter(cur)
                cur += index
                yield Command(cls.Token.REGISTER, parameter={'name': param, 'location': commands})
            elif "".join(token[0:3]) == cls.Token.CALL.value:
                cur += 3
                param, index = parameter(cur)
                cur += index
                yield Command(cls.Token.CALL, parameter={'name': param, 'location': commands})
            elif "".join(token[0:3]) == cls.Token.JUMP.value:
                cur += 3
                param, index = parameter(cur)
                cur += index
                yield Command(cls.Token.JUMP, parameter={'name': param})
            elif "".join(token[0:3]) == cls.Token.EQUAL.value:
                cur += 3
                param, index = parameter(cur)
                cur += index
                yield Command(cls.Token.EQUAL, parameter={'name': param})
            elif "".join(token[0:3]) == cls.Token.LESS.value:
                cur += 3
                param, index = parameter(cur)
                cur += index
                yield Command(cls.Token.LESS, parameter={'name': param})
            elif "".join(token[0:3]) == cls.Token.RETURN.value:
                cur += 3
                yield Command(cls.Token.RETURN)
            elif "".join(token[0:3]) == cls.Token.END.value:
                cur += 3
                yield Command(cls.Token.END)
            elif "".join(token[0:4]) == cls.Token.COUT.value:
                cur += 4
                yield Command(cls.Token.COUT)
            elif "".join(token[0:4]) == cls.Token.IOUT.value:
                cur += 4
                yield Command(cls.Token.IOUT)
            elif "".join(token[0:4]) == cls.Token.CIN.value:
                cur += 4
                yield Command(cls.Token.CIN)
            elif "".join(token[0:4]) == cls.Token.IIN.value:
                cur += 4
                yield Command(cls.Token.IIN)
            commands += 1

    @classmethod
    def characters(cls):
        return [" ", "\t", "\n"]
