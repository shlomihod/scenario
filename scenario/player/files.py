import shutil
import filecmp

def play_file_quote(quote):
    '''
    TODO: better names
    quote[0] - command
    quote[1] - exec env file path
    quote[2] - snr env file path
    quote[3] - exec full file path
    quote[4] - snr full file path
    '''

    if quote[0] == 'copy':
        shutil.copy(quote[4], quote[3])
        return False

    elif quote[0] == 'compare':
        if filecmp.cmp(quote[4], quote[3]):
            return True
        else:
            raise FileContentIncorrect()

def pre_scenario(pre_dialog):
    for index, (actor, quote) in enumerate(pre_dialog):
        if actor == 'F':
            play_file_quote(quote)
