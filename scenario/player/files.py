import os
import shutil
import filecmp

from scenario.player.exceptions import FileContentIncorrect, FileShouldNotExist, FileShouldExist, \
                                       OutputBeforeInput, ShouldEOF, ShouldOutputBeforeEOF, ShouldInputBeforeEOF


def compare_text_files(p1, p2):
    l1 = l2 = ' '
    with open(p1, 'rt') as f1, open(p2, 'rt') as f2:
        while l1 != '' and l2 != '':
            l1 = f1.readline()
            l2 = f2.readline()
            if l1 != l2:
                return False
    return True

def play_file_quote(quote):
    '''
    quote[0] - command

    2:
    quote[1] - exec env file path
    quote[2] - exec full file path

    4:
    quote[1] - exec env file path
    quote[2] - snr env file path
    quote[3] - exec full file path
    quote[4] - snr full file path
    '''

    if quote[0] == 'copy':
        if not os.path.exists(quote[4]):
            raise ValueError('{!r} not exsits'.format(quote[4]))

        if os.path.isdir(quote[4]):
            shutil.copytree(quote[4], quote[3])

        elif os.path.isfile(quote[4]):
            shutil.copy(quote[4], quote[3])

        else:
            raise ValueError('neither {!r} is neither a directory nor a file'.format(quote[4]))

        return False


    elif quote[0].startswith('compare'):

        if not os.path.exists(quote[4]):
            raise ValueError('{!r} not exsits'.format(quote[4]))

        if not os.path.exists(quote[3]):
            raise FileShouldExist()

        # first is backward compatibility
        if quote[0] == 'compare' or quote[0] == 'compare_binary':
            if filecmp.cmp(quote[4], quote[3]):
                return True
            else:
                raise FileContentIncorrect()

        # first is backward compatibility
        if quote[0] == 'compare_text':
            if compare_text_files(quote[4], quote[3]):
                return True
            else:
                raise FileContentIncorrect()


    elif quote[0] == 'exists':
        if not os.path.exists(quote[2]):
            raise FileShouldExist()
        
    elif quote[0] == 'not_exists':
        if os.path.exists(quote[2]):
            raise FileShouldNotExist()

def pre_scenario(pre_dialog):
    for index, (actor, quote) in enumerate(pre_dialog):
        if actor == 'F':
            play_file_quote(quote)
