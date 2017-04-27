import re
import string

import pexpect

from scenario.consts import VERBOSITY_DEFAULT, TIMEOUT_DEFAULT

from scenario.player.exceptions import FileContentIncorrect, FileShouldNotExist, FileShouldExist, \
                                       OutputBeforeInput, ShouldEOF, ShouldOutputBeforeEOF, ShouldInputBeforeEOF

from scenario.player.files import pre_scenario, play_file_quote

from scenario.player.feedback import generate_feedback_text, create_empty_feedback

def get_new_execution_text(p, with_after=True):
    text = p.before

    if with_after and isinstance(p.after, str):
        text += p.after

    return ('O', text)

def play_scenario(scenario, executable_path, verbosity=VERBOSITY_DEFAULT, timeout=TIMEOUT_DEFAULT, executable_extra_args=None):

    feedback = create_empty_feedback()
    
    feedback['name'] = scenario['name']
    
    def get_cleaned_before():
        if isinstance(p.before, str):

            if scenario['strictness']:

                before_lines = p.before.split('\r\n')
                if not any([set(l) - set(' ') for l in before_lines[:-1]]):
                    return before_lines[-1]
                else:
                    return p.before.strip('\r\n')
                
            else:
                return p.before.strip(' \r\n')

    def get_cleaned_after():
        if isinstance(p.after, str):

            if scenario['strictness']:

                #In STRICT mode, spaces in the end of the line are ignored
                after_lines = p.after.split('\r\n')
                if (after_lines and
                    not any([set(l) - set(' ') for l in after_lines[1:]])):
                    return after_lines[0].strip(' \r\n')
                else:
                    return p.after.strip('\r\n')
            
            else:
                return p.after.strip(' \r\n')

    pre_scenario(scenario['pre_dialog'])
    
    executable_path_with_snr_args = executable_path
    
    if scenario['args']:
        executable_path_with_snr_args += ' ' + scenario['args']
        feedback['args'] = '{!r}'.format(scenario['args'])
    
    if not executable_extra_args:
        p = pexpect.spawn(executable_path_with_snr_args, timeout=timeout, echo=False)
    
    else:
        executable_path_with_all_args = executable_path_with_snr_args + ' ' + executable_extra_args
        p = pexpect.spawn('/bin/bash', ['-c', executable_path_with_all_args], timeout=timeout, echo=False)
    
    
    try:
        for index, (actor, quote) in enumerate(scenario['dialog']):
            # is_warnings = False
            if actor in ['I', 'O']:
                
                if actor == 'O':
                    patterns = []

                    # Right spaces cannot be seen in run example
                    quote = quote.rstrip()

                    # if O is empty, then something need to be printed
                    if not quote:
                        escaped_quote = '.+\r\n'

                        pattern_quote = re.compile(escaped_quote)
                            
                        patterns.append(pattern_quote)

                    else:
                        escaped_quote = re.escape(quote)

                        pattern_quote = re.compile(escaped_quote)
                            
                        patterns.append(pattern_quote)

                        if not scenario['strictness']:
                                
                            pattern_cases = re.compile(escaped_quote, re.IGNORECASE)
                            patterns.append(pattern_cases)

                            # expand only spaces
                            #spaces_pattern_string = re.escape(' '.join(quote.split())).replace('\ ', '\s+')

                            # expand between every two chars
                            spaces_pattern_string = ' '.join(list(quote.replace(' ', '').
                                                                        replace('\t', '')))
                            spaces_pattern_string = re.escape(spaces_pattern_string)
                            spaces_pattern_string = spaces_pattern_string.replace('\ ', '\s*')

                            pattern_spaces = re.compile(spaces_pattern_string)
                            patterns.append(pattern_spaces)

                            pattern_cases_spaces = re.compile(spaces_pattern_string, re.IGNORECASE)
                            patterns.append(pattern_cases_spaces)
                        
                    try:                
                        index = p.expect(patterns)
                    except pexpect.EOF:
                        raise ShouldOutputBeforeEOF('')

                    
                    if not scenario['flow'] and get_cleaned_before():
                        raise pexpect.TIMEOUT('')
                    
                    
                    # NEED TO BE DOCUMENTED OR REFACTORED
                    _, text = get_new_execution_text(p)

                    if not scenario['flow']:
                        p.expect(['\r\n', pexpect.TIMEOUT, pexpect.EOF])
                        _, text_br = get_new_execution_text(p)
                        text += text_br
                    
                    # WHY DO I CHECK THAT \r\n IS NOT IN TEXT?!                    
                    if scenario['flow'] and '\r\n' not in text:
                        feedback['execution'].append(('O+', text ))
                    else:
                        feedback['execution'].append(('O', text ))
                    
                    if not scenario['flow'] and get_cleaned_before().strip(' '):
                        raise pexpect.TIMEOUT('')
                    
                    '''
                    if verbosity >= VERBOSITY['ERROR'] and index != 0:
                        if index == 1:
                            msg = 'Letter Cases'

                        if index == 2:
                            msg = 'Spaces'

                        if index == 3:
                            msg = 'Letter Cases & Spaces'     

                        feedback['warnings'].append('[{:02d}] [WARNNING] {!s} are not precise'.format(n_line, msg) )
                    '''

                elif actor == 'I':
                    p.expect(['.+', pexpect.TIMEOUT])

                    if not scenario['flow'] and get_cleaned_after():
                        raise OutputBeforeInput('')

                    if not p.isalive():
                        raise ShouldInputBeforeEOF('')

                    p.sendline(quote)
                    feedback['execution'].append(get_new_execution_text(p))
                    feedback['execution'].append(('I', quote))
                    
            elif actor == 'F':
                is_msg = play_file_quote(quote)

                if is_msg:
                        feedback['execution'].append(('F', 'Content of {!r} is correct'.format(quote[1])))

        if scenario['flow']:
            p.expect(['.+', pexpect.TIMEOUT, pexpect.EOF])
            _, text = get_new_execution_text(p)

            lines = string.split(text, '\r\n', maxsplit=1)
            if len(lines) > 0:
                feedback['execution'].append(('O+', lines[0] ))
                
                if len(lines) > 1 and lines[1]:
                    feedback['execution'].append(('O', lines[1] ))

            #feedback['execution'].append(get_new_execution_text(p))

        try:
            p.expect(pexpect.EOF)

            if not scenario['flow'] and get_cleaned_before():
                raise pexpect.TIMEOUT('')
                    
        except pexpect.TIMEOUT:
            raise ShouldEOF()

        feedback['result'] = True

    except pexpect.EOF:
        feedback['result'] = False
        
        feedback['execution'].append(get_new_execution_text(p))

        feedback['error'].append('the program finished too early')

    except pexpect.TIMEOUT:
        feedback['result'] = False

        #if scenario['flow']:
        feedback['execution'].append(get_new_execution_text(p))
            
        feedback['last'] = True
        feedback['error'].append('the program should have had this output instead:')
        feedback['error'].append('{!r}'.format(quote))


    except OutputBeforeInput:
        feedback['result'] = False

        feedback['execution'].append(get_new_execution_text(p, False))

        feedback['last'] = True
        feedback['error'].append('the program should not have output')
        feedback['error'].append('the program should get input')

    except ShouldInputBeforeEOF:
        feedback['result'] = False
        
        feedback['execution'].append(get_new_execution_text(p))

        feedback['error'].append('the program finished too early')
        feedback['error'].append('the program should get input')

    except ShouldOutputBeforeEOF:
        feedback['result'] = False

        feedback['execution'].append(get_new_execution_text(p))
        
        feedback['last'] = True
        feedback['error'].append('the program should have had this output before finishing:')
        feedback['error'].append('{!r}'.format(quote))

    except ShouldEOF:
        feedback['result'] = False

        feedback['execution'].append(get_new_execution_text(p))

        feedback['error'].append('the program should have finished')

        if not scenario['flow']:
            feedback['error'].append('instead the last line')
        
        feedback['error'].append('it might be that the program expects input, although it should not')

        '''
        if get_cleaned_before():
            feedback.append('[{:02d}] {!r}'.format(n_line+1, get_cleaned_before().split('\r\n')[0]))
        feedback.append('----> the program should have finished')
        if get_cleaned_before():
            feedback.append('----> instead the last line')
        '''

    except FileContentIncorrect:
        feedback['result'] = False

        feedback['error'].append('Content of file {!r} is incorrect'.format(quote[1]))
    

    except  FileShouldNotExist:
        feedback['result'] = False

        feedback['error'].append('File {!r} should not exist'.format(quote[1]))


    except FileShouldExist:
        feedback['result'] = False

        feedback['error'].append('File {!r} should exist'.format(quote[1]))
    
    p.close()
    feedback['exit_code'] = p.exitstatus
    feedback['signal_code'] = p.signalstatus

    # http://www.tldp.org/LDP/abs/html/exitcodes.html
    if 129 <= feedback['exit_code'] <= 162:
        feedback['signal_code'] = feedback['exit_code'] - 128
        feedback['exit_code'] = None

    if feedback['signal_code'] == 1:
        feedback['signal_code'] = None

    if feedback['signal_code'] is not None:
        feedback['result'] = False
        
    feedback_text = generate_feedback_text(feedback, verbosity)

    return feedback, feedback_text