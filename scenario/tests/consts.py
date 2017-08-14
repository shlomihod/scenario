__all__ = ['EXECUTABLE', 'DIALOUGE_PICES', 'ANNABEL_LEE']

import os

ANNABEL_LEE = '''It was many and many a year ago,
In a kingdom by the sea,
That a maiden there lived whom you may know
By the name of ANNABEL LEE;--
And this maiden she lived with no other thought
Than to love and be loved by me.
She was a child and I was a child,
In this kingdom by the sea,
But we loved with a love that was more than love--
I and my Annabel Lee--
With a love that the winged seraphs of heaven
Coveted her and me.'''

_executable_dirpath = os.path.dirname(os.path.abspath(__file__))
_executable_filepath = os.path.join(_executable_dirpath, 'executable.py')

EXECUTABLE = '{}'.format(_executable_filepath)

DIALOUGE_PIECES = {
    'output_all': [{
        'type': 'output',
        'name': 'poem line',
        'value': line
    } for line in ANNABEL_LEE.splitlines()],

    'output4': {
        'type': 'output',
        'name': 'poem line',
        'value': ANNABEL_LEE.splitlines()[4]
    },

    'output4_upper': {
        'type': 'output',
        'name': 'poem line',
        'value': ANNABEL_LEE.splitlines()[4].upper()
    },

    'input_comment': {
        'type': 'input',
        'name': 'comment',
        'value': 'A really nice poem!'
    },

    'output_comment': {
        'type': 'output',
        'name': 'comment',
        'value': 'A really nice poem!'
    },

    'output_poet':
    {
        'type': 'output',
        'name': 'poet',
        'value': 'Edgar Allan Poe'
    }
}