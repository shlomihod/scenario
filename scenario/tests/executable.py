#!/usr/bin/python

import sys
import ctypes

from scenario.tests.consts import ANNABEL_LEE


def crash():
    i = ctypes.c_char(b'a')
    j = ctypes.pointer(i)
    c = 0
    while True:
        j[c] = b'a'
        c += 1


if __name__ == '__main__':

    for arg in sys.argv[1:]:
        if arg == 'print':
            print(ANNABEL_LEE)

        elif arg == 'input':
            s = input('Enter Input: ')

        elif arg == 'output':
            print(s)

        elif arg == 'crash':
            crash()

        else:
            print('Wrong Argument ' + arg)
            sys.exit(1)
