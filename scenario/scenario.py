import pexpect

from _consts import ACTORS, VERBOSITY, VERBOSITY_DEFAULT, TIMEOUT_DEFAULT

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
                    raise pexpect.TIMEOUT(TIMEOUT)

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
            feedback.append('----> the program should have had this output insted:')
            feedback.append('----> {!r}'.format(quote))
        
        result = False

    else:
        try:
            p.expect(pexpect.EOF)

            if p.before.strip('\r\n'):
                raise pexpect.TIMEOUT(timeout)

        except pexpect.TIMEOUT:
            if verbosity >= VERBOSITY['ERROR']:
                if p.before.strip('\r\n'):
                    feedback.append('[{:02d}] {!r}'.format(index+2, p.before.strip('\r\n').split('\r\n')[0]))
                feedback.append('----> the program should have finished')
                if p.before.strip('\r\n'):
                    feedback.append('----> insted the last line')
                     
            
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

def run_scenario(executable_path, scenario_path, verbosity=VERBOSITY_DEFAULT, timeout=TIMEOUT_DEFAULT):

    scenario = parse_scenario_file(scenario_path)
    result, feedback = play_scenario(scenario, executable_path, verbosity, timeout)

    return result, feedback