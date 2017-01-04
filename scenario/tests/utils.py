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

import os as _os
_executable_dirpath = _os.path.dirname(_os.path.abspath(__file__))
_executable_filepath = _os.path.join(_executable_dirpath, 'executable.py')

EXECUTABLE = '{}'.format(_executable_filepath)