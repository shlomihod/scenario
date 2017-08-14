#!/usr/bin/python

import sys

from utils import ANNABEL_LEE

if __name__ == '__main__':

    for arg in sys.argv[1:]:
        if arg == 'print':
            print ANNABEL_LEE

        elif arg == 'input':
            s = raw_input('Enter Input: ')

        elif arg == 'output':
            print(s)

        else:
            print('Wrong Argument ' + arg)
            sys.exit(1)
