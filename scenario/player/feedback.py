from scenario.consts import VERBOSITY

def create_empty_feedback():
    return { 
            'name': '',
            'result': None,
            'exit_code': None,
            'signal_code': None,
            'args': '',
            'warnings': [],
            'last': False,
            'error': [],
            'execution': [],
           }

def f2t(s, e, is_repr=False):
    '''
    Feedback execution line to txt
    '''
    if isinstance(s, int):
        s = '{:02d}'.format(s)

    if is_repr:
        pattern = '[{!s}] {!r}'
    else:
        pattern = '[{!s}] {!s}'
    return pattern.format(s, e)

def generate_execution(feedback):
    i = 1
    last_output = []
    execution = []

    for a, e in feedback['execution']:
        if a == 'O':
            last_output = []
            for  l in e.splitlines():
                if l.strip():
                    last_output.append(f2t(i, l, True))
                    i += 1
            execution.extend(last_output)
        elif a == 'O+':
            if not execution or not execution[-1][1:3].isdigit():
                last_output = []
                last_output.append(f2t(i, e, True))
                execution.extend(last_output)
                i += 1
            else:
                last_output[-1] = last_output[-1][:-1] + e + "'"
                execution[-1] = execution[-1][:-1] + e + "'"
        elif a == 'I':
            execution.append(f2t('>>', e, True))

        elif a == 'F':
            execution.append(f2t('**', e))

    return execution, last_output

def generate_feedback_text(feedback, verbosity):

    feedback_text = []

    execution, last_output = generate_execution(feedback)

    if verbosity >= VERBOSITY['RESULT']:
        feedback_header = feedback['name'] + ' :: '
        if feedback['result']:
            feedback_header += 'SUCCESS'
        else:
            feedback_header += 'FAILED'

        feedback_text.append(feedback_header)
   
    if verbosity >= VERBOSITY['EXECUTION']:
        if feedback['args']:
            feedback_text.append(f2t('**', 'Arguments: ' + feedback['args'])) 
        feedback_text.extend(execution)


    if verbosity >= VERBOSITY['ERROR']:
        if verbosity == VERBOSITY['ERROR'] and feedback['last']:
            feedback_text.extend(last_output)

        feedback_text.extend(['---> ' + e for e in feedback['error']])

        if feedback['signal_code'] == 11:
            feedback_text.append('!!!! Segmentation Fault !!!!')

    if verbosity >= VERBOSITY['DEBUG']:
        feedback_text.append('EXIT CODE {}'.format(feedback['exit_code']))
        feedback_text.append('SIGNAL CODE {}'.format(feedback['signal_code']))

    feedback_text = '\n'.join(feedback_text)
    return feedback_text
