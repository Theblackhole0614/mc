from os import system
from typing import Callable
from random import random as rd, randint as rdi

from _variable import Variable, Type


class Builtin:
    def __init__(self, nb_params: int, func: Callable, ret: bool) -> None:
        self.nb_params = nb_params
        self.func = func
        self.ret = ret


def write(object: Variable) -> None:
    if object.vtype == Type.STRING:
        print(object.value, end='')
    else:
        print(object.value, end='')

def read() -> Variable:
    return Variable(Type.STRING, input())

def random() -> Variable:
    return Variable(Type.FLOAT, rd())

def randint(start: Variable, end: Variable) -> Variable:
    return Variable(Type.INT, rdi(start.value, end.value))

def strlen(string: Variable) -> Variable:
    return Variable(Type.INT, len(string.value))

def getchar(string: Variable, index: Variable) -> Variable:
    return Variable(Type.STRING, string.value[index.value])

def run(string: Variable) -> None:
    system(string.value)

built_ins = {
    'write': Builtin(1, write, False),
    'read': Builtin(0, read, True),
    'random': Builtin(0, random, True),
    'randint': Builtin(2, randint, True),
    'strlen': Builtin(1, strlen, True),
    'getchar': Builtin(2, getchar, True),
    'run': Builtin(1, run, False),
}
