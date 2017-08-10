# -*- coding: utf-8 -*-

import re
import string
import difflib
import copy
import json

import pexpect
import jsonschema

from scenario.consts import VERBOSITY_DEFAULT, TIMEOUT_DEFAULT, FEEDBACK_JSON_SCHEMA

from scenario.player.feedback_exceptions import SholdNoOutputBeforeInput, \
                                                ShouldEOF,                \
                                                ShouldOutputBeforeEOF,    \
                                                ShouldInputBeforeEOF,     \
                                                OutputIncorrect,          \
                                                EOFIncorrect,             \
                                                MemoryFeedbackError
                                    #FileContentIncorrect, FileShouldNotExist, FileShouldExist, \


#from scenario.player.files import pre_scenario, play_file_quote

from scenario.player.feedback import generate_feedback_text#, create_empty_feedback

from scenario.utils import xstr,                \
                           get_cleaned_before,  \
                           get_cleaned_after,   \
                           get_result_dict,     \
                           get_quote_type_dict, \
                           get_feedback_dict

def play_scenario(scenario, executable_path, verbosity=VERBOSITY_DEFAULT, timeout=TIMEOUT_DEFAULT, executable_extra_args=None):

    feedback = copy.deepcopy(scenario)
    feedback['log'] = {'quotes': [], 'text': ''}
    feedback['feedback'] = {'type': None, 'text': None}



    # pre_scenario(scenario['pre_dialogue'])

    executable_path_with_snr_args = executable_path

    if scenario['args']:
        executable_path_with_snr_args += ' ' + ' '.join(scenario['args'])

    if not executable_extra_args:
        p = pexpect.spawn(executable_path_with_snr_args, timeout=timeout, echo=False)

    else:
        executable_path_with_all_args = executable_path_with_snr_args + ' ' + executable_extra_args
        p = pexpect.spawn('/bin/bash', ['-c', executable_path_with_all_args], timeout=timeout, echo=False)


    try:
        for index, quote in enumerate(scenario['dialogue']):

            # is_warnings = False
            if quote['type'] in ['input', 'output']:

                if quote['type'] == 'output':
                    patterns = []

                    # Right spaces cannot be seen in run example
                    quote_value = quote['value'].rstrip()

                    # if output is empty, then something need to be printed
                    if not quote_value:
                        escaped_quote_value = '.+\r\n'

                        pattern_quote_value = re.compile(escaped_quote_value)

                        patterns.append(pattern_quote_value)

                    else:
                        escaped_quote_value = re.escape(quote_value)

                        pattern_quote_value = re.compile(escaped_quote_value)

                        patterns.append(pattern_quote_value)

                        if not scenario['strictness']:

                            pattern_cases = re.compile(escaped_quote_value, re.IGNORECASE)
                            patterns.append(pattern_cases)

                            # expand only spaces
                            #spaces_pattern_string = re.escape(' '.join(quote_value.split())).replace('\ ', '\s+')

                            # expand between every two chars
                            spaces_pattern_string = ' '.join(list(quote_value.replace(' ', '').
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
                        raise ShouldOutputBeforeEOF(quote)
                    except pexpect.TIMEOUT:
                        raise OutputIncorrect(quote)

                    # BEFORE the quote match
                    if not scenario['flow'] and get_cleaned_before(p, scenario['strictness']):
                        raise OutputIncorrect(quote)

                    else:
                        feedback['log']['quotes'].append({ 'type': get_quote_type_dict('printing'),
                                                 'value': p.before,
                                                 })
                    # THE MATCH of the quote
                    assert p.after is not None
                    feedback['log']['quotes'].append({ 'type': get_quote_type_dict('output'),
                                             'name': quote['name'],
                                             'value': p.after,
                                             })

                    # AFTER the quote match UNTIL THE END OF THE LINE
                    p.expect(['\r\n', pexpect.TIMEOUT, pexpect.EOF])

                    if not scenario['flow']:
                        feedback['log']['quotes'].append({ 'type': get_quote_type_dict('printing'),
                                                 'value': p.before + xstr(p.after)
                                                 })

                        if get_cleaned_before(p, scenario['strictness']).strip(' '):
                            raise OutputIncorrect(quote)


                    else:
                        feedback['log']['quotes'].append({ 'type': get_quote_type_dict('printing'),
                                                 'value': p.before + p.after
                                                 })

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

                elif quote['type'] == 'input':
                    try:
                        p.expect(['.+', pexpect.TIMEOUT])
                    except pexpect.EOF:
                        raise EOFIncorrect(quote)

                    feedback['log']['quotes'].append({ 'type': get_quote_type_dict('printing'),
                                             'value': p.before + xstr(p.after)
                                             })


                    if not scenario['flow'] and get_cleaned_after(p, scenario['strictness']):
                        raise SholdNoOutputBeforeInput(quote)

                    if not p.isalive():
                        raise ShouldInputBeforeEOF(quote)

                    p.sendline(quote['value'])

                    quote['type'] = get_quote_type_dict('input')
                    feedback['log']['quotes'].append(quote)# ('I', quote))
            '''
            elif actor == 'F':
                is_msg = play_file_quote(quote)

                if is_msg:
                        feedback['log']['quotes'].append(('F', 'Content of {!r} is correct'.format(quote[1])))
            '''
        if scenario['flow']:
            p.expect(['.+', pexpect.TIMEOUT, pexpect.EOF])

            feedback['log']['quotes'].append({ 'type': get_quote_type_dict('printing'),
                                    'value': p.before + xstr(p.after)
                                 })
            '''
            _, text = get_new_execution_text(p)

            lines = string.split(text, '\r\n', maxsplit=1)
            if len(lines) > 0:
                feedback['log']['quotes'].append(('O+', lines[0] ))

                if len(lines) > 1 and lines[1]:
                    feedback['log']['quotes'].append(('O', lines[1] ))

            #feedback['log']['quotes'].append(get_new_execution_text(p))
            '''

        try:
            p.expect(pexpect.EOF)

            if not scenario['flow'] and get_cleaned_before(p, scenario['strictness']):
                raise pexpect.TIMEOUT

        except pexpect.TIMEOUT:
            raise ShouldEOF(quote)

        feedback['result'] = get_result_dict(True)
        feedback['feedback'] = get_feedback_dict(None)

    ### REAL FEEDBACK EXCEPTIONS PART ###

    except EOFIncorrect:
        feedback['result'] = get_result_dict(False)

        feedback['log']['quotes'].append({ 'type': get_quote_type_dict('printing'),
                                'value': p.before + xstr(p.after)
                             })

        feedback['feedback'] = get_feedback_dict(e)

    except OutputIncorrect as e:
        feedback['result'] = get_result_dict(False)

        #if scenario['flow']:
        feedback['log']['quotes'].append({ 'type': get_quote_type_dict('printing'),
                                'value': p.before + xstr(p.after)
                             })

#        feedback['last'] = True
        feedback['feedback'] = get_feedback_dict(e)
        #feedback['feedback'].append('{!r}'.format(quote))


    except SholdNoOutputBeforeInput as e:
        feedback['result'] = get_result_dict(False)

        feedback['log']['quotes'].append({ 'type': get_quote_type_dict('printing'),
                                'value': p.before
                             })

        feedback['last'] = True
        feedback['feedback'] = get_feedback_dict(e)
        #feedback['feedback'].append('the program should get input')

    except ShouldInputBeforeEOF as e:
        feedback['result'] = get_result_dict(False)

        feedback['log']['quotes'].append({ 'type': get_quote_type_dict('printing'),
                                'value': p.before + xstr(p.after)
                             })

        feedback['feedback'] = get_feedback_dict(e)
        #feedback['feedback'].append('the program should get input')

    except ShouldOutputBeforeEOF as e:
        feedback['result'] = get_result_dict(False)

        feedback['log']['quotes'].append({ 'type': get_quote_type_dict('printing'),
                                'value': p.before + xstr(p.after)
                             })

        feedback['last'] = True
        feedback['feedback'] = get_feedback_dict(e)
        #feedback['feedback'].append('{!r}'.format(quote))

    except ShouldEOF as e:
        feedback['result'] = get_result_dict(False)

        feedback['log']['quotes'].append({ 'type': get_quote_type_dict('printing'),
                                'value': p.before + xstr(p.after)
                             })

        #feedback['feedback'] = ('the program should have finished')

        if not scenario['flow']:
            pass
            #feedback['feedback'].append('instead the last line')

        feedback['feedback'] = get_feedback_dict(e)

        '''
        if get_cleaned_before(p, scenario['strictness']):
            feedback.append('[{:02d}] {!r}'.format(n_line+1, get_cleaned_before(p, scenario['strictness']).split('\r\n')[0]))
        feedback.append('----> the program should have finished')
        if get_cleaned_before(p, scenario['strictness']):
            feedback.append('----> instead the last line')
        '''
    '''
    except FileContentIncorrect:
        feedback['result'] = False

        feedback['feedback'].append('Content of file {!r} is incorrect'.format(quote[1]))

        feedback['feedback'].append('')
        feedback['feedback'].append('Diff executable file VS. scenario file:')

        exec_file_content = open(quote[3], 'U').readlines()
        snr_file_content = open(quote[4], 'U').readlines()
        diff = difflib.ndiff(exec_file_content, snr_file_content)

        feedback['feedback'].extend(''.join(diff).splitlines())

    except  FileShouldNotExist:
        feedback['result'] = False

        feedback['feedback'].append('File {!r} should not exist'.format(quote[1]))


    except FileShouldExist:
        feedback['result'] = False

        feedback['feedback'].append('File {!r} should exist'.format(quote[1]))
    '''

    p.close()
    feedback['exit_code'] = p.exitstatus
    feedback['signal_code'] = p.signalstatus

    # http://www.tldp.org/LDP/abs/html/exitcodes.html
    if 129 <= feedback['exit_code'] <= 162:
        feedback['signal_code'] = feedback['exit_code'] - 128
        feedback['exit_code'] = None

    if feedback['signal_code'] == 0:
        feedback['signal_code'] = None

    # WHY?
    if feedback['signal_code'] == 1:
        feedback['signal_code'] = None

    if feedback['signal_code'] is not None:
        feedback['result'] = get_result_dict(False)
        feedback['feedback'] = get_feedback_dict(MemoryFeedbackError())

    for quote in feedback['log']['quotes']:
        if quote['type']['en'] == 'output':
            feedback['log']['text'] += '<'
        feedback['log']['text'] += quote['value']
        if quote['type']['en'] == 'output':
            feedback['log']['text'] += '>'

        if quote['type']['en'] == 'input':
            feedback['log']['text'] += '\r\n'

    jsonschema.validate(feedback, FEEDBACK_JSON_SCHEMA)

    return feedback
