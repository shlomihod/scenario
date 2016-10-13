import pexpect

TIMEOUT = 1
ACTORS = list('NRAIO')

def parse_scenario_line(scenario_line):
    parts = tuple(scenario_line.split(': ', 1))

    assert len(parts) == 2, 'Each line should be in the format of <actor>: <quote>'
    assert parts[0] in ACTORS, '{} is not recognized actor (Only {})' \
                                .format(parts[0], ACTORS)

    return parts

def parse_scenario_file(scenario_path):
    with open(scenario_path, 'r') as f:
        lines = f.read().splitlines()

    name = ''
    args = ''
    dialog = []

    assert len(lines) != 0, 'Scenario file cannot be empty'

    parsed_line = parse_scenario_line(lines[0])
    assert parsed_line[0] == 'N', 'Frist line sholud be Name'
    assert parsed_line[1].strip() != '', 'Cannot be empty name'
    name = parsed_line[1].strip()

    try:
        for i, line in enumerate(lines[1:]):
            
                parsed_line = parse_scenario_line(line)

                if parsed_line[0] == 'R':
                    continue
                
                elif parsed_line[0] == 'A':
                    assert args == '', 'Cannot be more than one A actor'
                    args = parsed_line[1]
                
                else:
                    dialog.append(parsed_line)

    except AssertionError as e:
        raise RuntimeError('Error in scenario file at line {}: {}' \
                            .format(i, e))

    return {'name': name, 'args': args, 'dialog': dialog}

def play_scenario(scenario, executable_path, verbose=False):

    result = None

    feedback = ''
    feedback_header = ''
    feedback_comments = []
    feedback_runlog = []
    

    executable_path_with_args = executable_path + ' '+ scenario['args']
    
    p = pexpect.spawn(executable_path_with_args, timeout=TIMEOUT, echo=False)

    try:
        for index, (actor, quote) in enumerate(scenario['dialog']):
            
            if actor == 'O':
                p.expect_exact(quote)

                if p.before.strip('\r\n') != '':
                    raise pexpect.TIMEOUT(TIMEOUT)

            elif actor == 'I':
                if not p.isalive():
                    raise pexpect.EOF(TIMEOUT)

                p.sendline(quote)

            feedback_runlog.append('<OK> {!r}'.format(quote))

    except pexpect.EOF:
        feedback_comments.append('the program finised too early')
        feedback_comments.append('at line:')
        feedback_comments.append('{!r}'.format(quote))
        result = False

    except pexpect.TIMEOUT:
        feedback_comments.append('the program should have had this output:')
        feedback_comments.append('{!r}'.format(quote))
        feedback_comments.append('but the program output was:')
        feedback_comments.append('{!r}'.format(p.before.strip('\r\n')))
        result = False

    else:
        try:
            p.expect(pexpect.EOF)

            if p.before.strip('\r\n'):
                raise pexpect.TIMEOUT(TIMEOUT)

        except pexpect.TIMEOUT:
            feedback_comments.append('the program should have finished')
            if p.before.strip('\r\n'):
                feedback_comments.append('but the program output was:')
                feedback_comments.append('{!r}'.format(p.before.strip('\r\n')))
            result = False

        else:
            feedback_runlog.append('<EXIT CODE> {}'.format(p.exitstatus))
            result = True

    feedback_header += scenario['name'] + ' :: '
    if result:
        feedback_header += 'SUCCESS'
    else:
        feedback_header += 'FAILED'

    feedback += feedback_header + '\n'

    feedback += '\n'.join(['\t' + line for line in feedback_comments])
    
    if verbose:
        feedback += '\n'.join(['VERBOSE ' + line for line in feedback_runlog])
    
    return result, feedback

def run_scenario(executable_path, scenario_path, verbose=False):

    scenario = parse_scenario_file(scenario_path)
    result, feedback = play_scenario(scenario, executable_path, verbose)

    return result, feedback