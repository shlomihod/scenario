#!/usr/bin/python

import sys

from utils import ANNABEL_LEE

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Only one arg allowed'
        sys.exit(1)

    if sys.argv[1] == 'print':
        print ANNABEL_LEE

    elif sys.argv[1] == 'print_input':
        print ANNABEL_LEE
        raw_input()

    elif sys.argv[1] == 'print_print-input':
        print ANNABEL_LEE
        print raw_input()

    elif sys.argv[1] == 'print-input':
        print raw_input()

    elif sys.argv[1] == 'print-cases-spaces_print-input':
        text = ANNABEL_LEE[:].splitlines()
        text[3] = text[3].upper()
        text[4] = text[4].replace(' ', '  ')
        text[5] = text[5] + '    ' 
        text[6] = text[6].lower().replace(' ', '  ')
        text = '\n'.join(text)
        print text
        print raw_input()

    elif sys.argv[1] == 'extra-spaces-beginning-line-print_input':
        text = ANNABEL_LEE[:].splitlines()
        text[3] = '    ' + text[3]
        text = '\n'.join(text)
        print text
        print raw_input()

    elif sys.argv[1] == 'extra-spaces-end-line-print_input':
        text = ANNABEL_LEE[:].splitlines()
        text[3] = text[3] + '    '
        text = '\n'.join(text)
        print text
        print raw_input()

    elif sys.argv[1] == 'extra-spaces-end-print_input':
        text = ANNABEL_LEE[:] + '     '
        print text
        print raw_input()

    else:
        print 'Arguement not allowed'