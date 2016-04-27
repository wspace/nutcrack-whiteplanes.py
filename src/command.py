#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from enum import Enum


########################################################################
# Push
########################################################################
class Push(object):

    Token, Step, IsNeedParameter = "  ", 2, True

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the PUSH command. """
        context.stack.append(int(parameter['param'], 2))


########################################################################
# Copy
########################################################################
class Copy(object):

    Token, Step, IsNeedParameter = " \t ", 3, True

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the COPY command. """
        index = int(parameter['param'], 2)
        context.stack.append(context.stack[index])


########################################################################
# Slide
########################################################################
class Slide(object):

    Token, Step, IsNeedParameter = " \t\n", 3, True

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the SLIDE command. """
        value = context.stack.pop()
        for index in range(0, int(parameter['param'], 2)):
            context.stack.pop()
        context.stack.append(value)


########################################################################
# Duplicate
########################################################################
class Duplicate(object):

    Token, Step, IsNeedParameter = " \n ", 3, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the DUPLICATE command. """
        context.stack.append(context.stack[-1])


########################################################################
# Swap
########################################################################
class Swap(object):

    Token, Step, IsNeedParameter = " \n\t", 3, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the SWAP command. """
        c = context
        c.stack[-1], c.stack[-2] = c.stack[-2], c.stack[-1]


########################################################################
# Discard
########################################################################
class Discard(object):

    Token, Step, IsNeedParameter = " \n\n", 3, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the DISCARD command. """
        context.stack.pop()


########################################################################
# Add
########################################################################
class Add(object):

    Token, Step, IsNeedParameter = "\t   ", 4, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the ADD command. """
        lhs, rhs = context.stack.pop(), context.stack.pop()
        context.stack.append(lhs + rhs)


########################################################################
# Sub
########################################################################
class Sub(object):

    Token, Step, IsNeedParameter = "\t  \t", 4, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the SUB command. """
        lhs, rhs = context.stack.pop(), context.stack.pop()
        context.stack.append(lhs - rhs)


########################################################################
# Mul
########################################################################
class Mul(object):

    Token, Step, IsNeedParameter = "\t  \n", 4, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the MUL command. """
        lhs, rhs = context.stack.pop(), context.stack.pop()
        context.stack.append(lhs * rhs)


########################################################################
# Div
########################################################################
class Div(object):

    Token, Step, IsNeedParameter = "\t \t ", 4, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the DIV command. """
        lhs, rhs = context.stack.pop(), context.stack.pop()
        context.stack.append(lhs / rhs)


########################################################################
# Mod
########################################################################
class Mod(object):

    Token, Step, IsNeedParameter = "\t \t\t", 4, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the MOD command. """
        lhs, rhs = context.stack.pop(), context.stack.pop()
        context.stack.append(lhs % rhs)


########################################################################
# Store
########################################################################
class Store(object):

    Token, Step, IsNeedParameter = "\t\t ", 3, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the STORE command. """
        value, address = context.stack.pop(), context.stack.pop()
        context.heap[address] = value


########################################################################
# Retrieve
########################################################################
class Retrieve(object):

    Token, Step, IsNeedParameter = "\t\t\t", 3, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the RETRIEVE command. """
        address = context.stack.pop()
        context.stack.append(context.heap[address])


########################################################################
# Register
########################################################################
class Register(object):

    Token, Step, IsNeedParameter = "\n  ", 3, True

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the REGISTER command. """
        context.labels[parameter['param']] = parameter['location']


########################################################################
# Call
########################################################################
class Call(object):

    Token, Step, IsNeedParameter = "\n \t", 3, True

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the CALL command. """
        context.callstack.append(parameter['location'])
        context.counter = context.labels[parameter['param']]


########################################################################
# Jump
########################################################################
class Jump(object):

    Token, Step, IsNeedParameter = "\n \n", 3, True

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the JUMP command. """
        context.counter = context.labels[parameter['param']]


########################################################################
# Equal
########################################################################
class Equal(object):

    Token, Step, IsNeedParameter = "\n\t ", 3, True

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the TEST[EQUAL] command. """
        if context.stack.pop() == 0:
            context.counter = context.labels[parameter['param']]


########################################################################
# Less
########################################################################
class Less(object):

    Token, Step, IsNeedParameter = "\n\t\t", 3, True

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the TEST[LESS] command. """
        if context.stack.pop() < 0:
            context.counter = context.labels[parameter['param']]


########################################################################
# Return
########################################################################
class Return(object):

    Token, Step, IsNeedParameter = "\n\t\n", 3, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the RETURN command. """
        context.counter = context.callstack.pop()


########################################################################
# End
########################################################################
class End(object):

    Token, Step, IsNeedParameter = "\n\n\n", 3, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the END command. """
        context.counter = sys.maxsize - 1


########################################################################
# Cout
########################################################################
class Cout(object):

    Token, Step, IsNeedParameter = "\t\n  ", 4, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the OUTPUT[CHARACTER] command. """
        value = context.stack.pop()
        context.output(chr(value))


########################################################################
# Iout
########################################################################
class Iout(object):

    Token, Step, IsNeedParameter = "\t\n \t", 4, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the OUTPUT[INT] command. """
        value = context.stack.pop()
        context.output(value)


########################################################################
# Cin
########################################################################
class Cin(object):

    Token, Step, IsNeedParameter = "\t\n\t ", 4, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the INPUT[CHARACTER] command. """
        address = context.stack.pop()
        value = context.input("CIN")
        context.heap[address] = ord(value)


########################################################################
# Iin
########################################################################
class Iin(object):

    Token, Step, IsNeedParameter = "\t\n\t\t", 4, False

    @classmethod
    def process(cls, *, context=None, parameter=None):
        """ Evaluate the INPUT[INT] command. """
        address = context.stack.pop()
        value = context.input("IIN")
        context.heap[address] = value


########################################################################
# Command
########################################################################
class Command(object):

    def __init__(self, name, *, parameter=None):
        self.name = name
        self.parameter = parameter

    def __call__(self, *, context=None):
        self.name.process(context=context, parameter=self.parameter)

    @classmethod
    def make(cls, code):
        cur, commands, count = 0, 0, len(code)
        while cur < count:
            token = code[cur:] if ((cur + 3) - count) >= 0 else code[cur:cur + 4]
            if "".join(token[0:Push.Step]) == Push.Token:
                cur += Push.Step
                param, index = cls.parameter(code, cur)
                cur += index
                yield Command(Push, parameter={'param': param})
            elif "".join(token[0:Copy.Step]) == Copy.Token:
                cur += Copy.Step
                param, index = cls.parameter(code, cur)
                cur += index
                yield Command(Copy, parameter={'param': param})
            elif "".join(token[0:Slide.Step]) == Slide.Token:
                cur += Slide.Step
                param, index = cls.parameter(code, cur)
                cur += index
                yield Command(Slide, parameter={'param': param})
            elif "".join(token[0:Duplicate.Step]) == Duplicate.Token:
                cur += Duplicate.Step
                yield Command(Duplicate)
            elif "".join(token[0:Swap.Step]) == Swap.Token:
                cur += Swap.Step
                yield Command(Swap)
            elif "".join(token[0:Discard.Step]) == Discard.Token:
                cur += Discard.Step
                yield Command(Discard)
            elif "".join(token[0:Add.Step]) == Add.Token:
                cur += Add.Step
                yield Command(Add)
            elif "".join(token[0:Sub.Step]) == Sub.Token:
                cur += Sub.Step
                yield Command(Sub)
            elif "".join(token[0:Mul.Step]) == Mul.Token:
                cur += Mul.Step
                yield Command(Mul)
            elif "".join(token[0:Div.Step]) == Div.Token:
                cur += Div.Step
                yield Command(Div)
            elif "".join(token[0:Mod.Step]) == Mod.Token:
                cur += Mod.Step
                yield Command(Mod)
            elif "".join(token[0:Store.Step]) == Store.Token:
                cur += Store.Step
                yield Command(Store)
            elif "".join(token[0:Retrieve.Step]) == Retrieve.Token:
                cur += Retrieve.Step
                yield Command(Retrieve)
            elif "".join(token[0:Register.Step]) == Register.Token:
                cur += Register.Step
                param, index = cls.parameter(code, cur)
                cur += index
                yield Command(Register, parameter={'param': param, 'location': commands})
            elif "".join(token[0:Call.Step]) == Call.Token:
                cur += Call.Step
                param, index = cls.parameter(code, cur)
                cur += index
                yield Command(Call, parameter={'param': param, 'location': commands})
            elif "".join(token[0:Jump.Step]) == Jump.Token:
                cur += Jump.Step
                param, index = cls.parameter(code, cur)
                cur += index
                yield Command(Jump, parameter={'param': param})
            elif "".join(token[0:Equal.Step]) == Equal.Token:
                cur += Equal.Step
                param, index = cls.parameter(code, cur)
                cur += index
                yield Command(Equal, parameter={'param': param})
            elif "".join(token[0:Less.Step]) == Less.Token:
                cur += Less.Step
                param, index = cls.parameter(code, cur)
                cur += index
                yield Command(Less, parameter={'param': param})
            elif "".join(token[0:Return.Step]) == Return.Token:
                cur += Return.Step
                yield Command(Return)
            elif "".join(token[0:End.Step]) == End.Token:
                cur += End.Step
                yield Command(End)
            elif "".join(token[0:Cout.Step]) == Cout.Token:
                cur += Cout.Step
                yield Command(Cout)
            elif "".join(token[0:Iout.Step]) == Iout.Token:
                cur += Iout.Step
                yield Command(Iout)
            elif "".join(token[0:Cin.Step]) == Cin.Token:
                cur += Cin.Step
                yield Command(Cin)
            elif "".join(token[0:Iin.Step]) == Iin.Token:
                cur += Iin.Step
                yield Command(Iin)
            commands += 1

    @classmethod
    def parameter(cls, code, index):
        param = ""
        for character in code[index:]:
            if character == " ":
                param += "0"
            elif character == "\t":
                param += "1"
            elif character == "\n":
                return (param, len(param) + 1)

    @classmethod
    def characters(cls):
        return [" ", "\t", "\n"]
