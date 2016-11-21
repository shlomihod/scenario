import pexpect

from _consts import VERBOSITY, VERBOSITY_DEFAULT, TIMEOUT_DEFAULT

def play_scenario(scenario, executable_path, verbosity=VERBOSITY_DEFAULT, timeout=TIMEOUT_DEFAULT):

    result = None

    feedback = []

    executable_path_with_args = executable_path + ' '+ scenario['args']
    
    p = pexpect.spawn(executable_path_with_args, timeout=timeout, echo=False)

    try:
        for index, (actor, quote) in enumerate(scenario['dialog']):
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

            if verbosity >=3:
                feedback.append('[{:02d}] {!r}'.format(index+1, quote))

    except pexpect.EOF:
        if verbosity >= VERBOSITY['ERROR']:
            feedback.append('----> the program finised too early')

        result = False

    except pexpect.TIMEOUT:
        if verbosity >= VERBOSITY['ERROR']:
            feedback.append('[{:02d}] {!r}'.format(index+1, p.before.strip('\r\n').split('\r\n')[0]))
            feedback.append('----> the program should have had this output instead:')
            feedback.append('----> {!r}'.format(quote))
        
        result = False

    else:
        try:
            p.expect(pexpect.EOF)

            if p.before.strip('\r\n'):
                raise pexpect.TIMEOUT('')

        except pexpect.TIMEOUT:
            if verbosity >= VERBOSITY['ERROR']:
                if p.before.strip('\r\n'):
                    feedback.append('[{:02d}] {!r}'.format(index+2, p.before.strip('\r\n').split('\r\n')[0]))
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
