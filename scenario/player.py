import shutil
import filecmp

import pexpect

from _consts import VERBOSITY, VERBOSITY_DEFAULT, TIMEOUT_DEFAULT

class FileContentIncorrect(Exception):
    pass

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

def play_scenario(scenario, executable_path, verbosity=VERBOSITY_DEFAULT, timeout=TIMEOUT_DEFAULT):

    result = None

    feedback = []

    executable_path_with_args = executable_path + ' '+ scenario['args']
    
    p = pexpect.spawn(executable_path_with_args, timeout=timeout, echo=False)

    n_line = 0

    try:
        for index, (actor, quote) in enumerate(scenario['dialog']):
            if actor in ['I', 'O']:
                n_line += 1
                if actor == 'O':
                    try:
                        p.expect_exact(quote)

                    except pexpect.EOF:
                        if p.before.strip('\r\n'):
                            raise pexpect.TIMEOUT('')

                        else:
                            raise pexpect.EOF('')

                    if p.before.strip('\r\n') != '':
                        raise pexpect.TIMEOUT('')

                elif actor == 'I':
                    if not p.isalive():
                        raise pexpect.EOF('')

                    p.sendline(quote)
                
                if verbosity >= VERBOSITY['EXECUTION']:
                    feedback.append('[{:02d}] {!r}'.format(n_line, quote))

            elif actor == 'F':
                is_msg = play_file_quote(quote)

                if is_msg:
                    if verbosity >= VERBOSITY['EXECUTION']:
                        feedback.append('[**] Content of file {!r} is correct'.format(quote[1]))

    except pexpect.EOF:
        if verbosity >= VERBOSITY['ERROR']:
            feedback.append('----> the program finised too early')

        result = False

    except pexpect.TIMEOUT:
        if verbosity >= VERBOSITY['ERROR']:
            feedback.append('[{:02d}] {!r}'.format(n_line, p.before.strip('\r\n').split('\r\n')[0]))
            feedback.append('----> the program should have had this output instead:')
            feedback.append('----> {!r}'.format(quote))
        
        result = False

    except FileContentIncorrect:
        result = False
        if verbosity >= VERBOSITY['ERROR']:
            feedback.append('----> Content of file {!r} is incorrect'.format(quote[1]))

    else:
        try:
            p.expect(pexpect.EOF)

            if p.before.strip('\r\n'):
                raise pexpect.TIMEOUT('')

        except pexpect.TIMEOUT:
            if verbosity >= VERBOSITY['ERROR']:
                if p.before.strip('\r\n'):
                    feedback.append('[{:02d}] {!r}'.format(n_line+1, p.before.strip('\r\n').split('\r\n')[0]))
                feedback.append('----> the program should have finished')
                if p.before.strip('\r\n'):
                    feedback.append('----> instead the last line')
                     
            
            result = False

        else:
            if verbosity >= VERBOSITY['DEBUG']:
                feedback.append('EXIT CODE {}'.format(p.exitstatus))
            
            result = True

    if verbosity >= VERBOSITY['RESULT']:
        feedback_header = scenario['name'] + ' :: '
        if result:
            feedback_header += 'SUCCESS'
        else:
            feedback_header += 'FAILED'

        feedback.insert(0, feedback_header)

    feedback = '\n'.join([line for line in feedback])

    return result, feedback
