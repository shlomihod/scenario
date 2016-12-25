import shutil
import filecmp
import re

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

def pre_scenario(pre_dialog):
    for index, (actor, quote) in enumerate(pre_dialog):
        if actor == 'F':
            play_file_quote(quote)

def play_scenario(scenario, executable_path, verbosity=VERBOSITY_DEFAULT, timeout=TIMEOUT_DEFAULT):

    result = None

    feedback = []
    
    def get_cleaned_before():
        if scenario['strictness']:
            return p.before.strip('\r\n')
        else:
            return p.before.strip(' \r\n')

    pre_scenario(scenario['pre_dialog'])
    
    executable_path_with_args = executable_path
    
    if scenario['args']:
        executable_path_with_args += ' ' + scenario['args']
        if verbosity >= VERBOSITY['EXECUTION']:
            feedback.append('[**] Arguments: {!r}'.format(scenario['args']))
    
    p = pexpect.spawn(executable_path_with_args, timeout=timeout, echo=False)

    n_line = 0

    try:
        for index, (actor, quote) in enumerate(scenario['dialog']):
            is_warnings = False

            if actor in ['I', 'O']:
                n_line += 1
                if actor == 'O':
                    try:
                        if scenario['strictness']:
                            p.expect_exact(quote)

                        else:
                            escaped_quote = re.escape(quote)
                            pattern_quote = re.compile(escaped_quote)
                            pattern_cases = re.compile(escaped_quote, re.IGNORECASE)
                            
                            spaces_pattern_string = re.escape(' '.join(quote.split())).replace('\ ', '\s+')
                            pattern_spaces = re.compile(spaces_pattern_string)
                            pattern_cases_spaces = re.compile(spaces_pattern_string, re.IGNORECASE)
                            
                            index = p.expect([pattern_quote, pattern_cases, pattern_spaces, pattern_cases_spaces])
                            if verbosity >= VERBOSITY['ERROR'] and index != 0:
                                if index == 1:
                                    msg = 'Letter Cases'
                                if index == 2:
                                    msg = 'Spaces'
                                if index == 3:
                                    msg = 'Letter Cases & Spaces'     
                                feedback.append('[{:02d}] [WARNNING] {!s} are not correct'.format(n_line, msg) )

                    except pexpect.EOF:
                        if get_cleaned_before():
                            raise pexpect.TIMEOUT('')

                        else:
                            raise pexpect.EOF('')
                    if get_cleaned_before():
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
                        feedback.append('[**] [FILE] Content of {!r} is correct'.format(quote[1]))

    except pexpect.EOF:
        if verbosity >= VERBOSITY['ERROR']:
            feedback.append('----> the program finised too early')

        result = False

    except pexpect.TIMEOUT:
        if verbosity >= VERBOSITY['ERROR']:
            feedback.append('[{:02d}] {!r}'.format(n_line, get_cleaned_before().split('\r\n')[0]))
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
            if get_cleaned_before():
                raise pexpect.TIMEOUT('')

        except pexpect.TIMEOUT:
            if verbosity >= VERBOSITY['ERROR']:
                if get_cleaned_before():
                    feedback.append('[{:02d}] {!r}'.format(n_line+1, get_cleaned_before().split('\r\n')[0]))
                feedback.append('----> the program should have finished')
                if get_cleaned_before():
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

    feedback = '\n'.join([line for line in feedback]) + '\n'

    return result, feedback
