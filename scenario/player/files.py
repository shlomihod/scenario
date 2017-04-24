import os
import shutil
import filecmp

from scenario.player.exceptions import FileContentIncorrect, FileShouldNotExist, FileShouldExist, \
                                       OutputBeforeInput, ShouldEOF, ShouldOutputBeforeEOF, ShouldInputBeforeEOF

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
        shutil.copy(quote[4], quote[3])
        return False

    elif quote[0] == 'compare':
        if not os.path.exists(quote[3]):
            raise FileShouldExist()

        if filecmp.cmp(quote[4], quote[3]):
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
