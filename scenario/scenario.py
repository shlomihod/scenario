import pexpect

TIMEOUT = 1
ACTORS = list('RAIO')

def parse_scenario_line(scenario_line):
    parts = tuple(scenario_line.split(': ', 1))

    assert len(parts) == 2, 'Each line should be in the format of <actor>: <quote>'
    assert parts[0] in ACTORS, '{} is not recognized actor (Only {})' \
                                .format(parts[0], ACTORS)

    return parts

def parse_scenario_file(scenario_path):
    with open(scenario_path, 'r') as f:
        lines = f.read().splitlines()

    args = ''
    dialog = []

    try:
        for i, line in enumerate(lines):
            
                parsed_line = parse_scenario_line(line)

                if parsed_line[0] == 'R':
                    continue
                
                elif parsed_line[0] == 'A':
                    assert args == '', "Cannot be more than one A actor"
                    args = parsed_line[1]
                
                else:
                    dialog.append(parsed_line)

    except AssertionError as e:
        raise RuntimeError('Error in scenario file at line {}: {}' \
                            .format(i, e))

    return {'args': args, 'dialog': dialog}

def play_scenario(scenario, executable_path):

    result = None
    feedback = ''

    executable_path_with_args = executable_path + ' '+ scenario['args']

    feedback += 'executing {}\n'.format(executable_path_with_args)
    
    p = pexpect.spawn(executable_path_with_args, timeout=TIMEOUT, echo=False)

    try:
        for index, (actor, quote) in enumerate(scenario['dialog']):
            if actor == 'O':
                p.expect_exact(quote)
                if p.before.strip('\r\n') != '':
                    raise pexpect.TIMEOUT(TIMEOUT)

            elif actor == 'I':
                p.sendline(quote)

            feedback += 'ok {!r}\n'.format(quote)

    except pexpect.EOF:
        feedback += 'not ok TOO EARLY END OF EXECUTION\n'
        feedback += '---at {!r}\n'.format(quote)
        feedback += 'FAILED!\n'
        result = False

    except pexpect.TIMEOUT:
        feedback += 'not ok MISMATCH\n'
        feedback += '---should be {!r}\n'.format(quote)
        feedback += '---but got   {!r}\n'.format(p.before.strip('\r\n'))
        feedback += 'FAILED!\n'
        result = False

    else:
        try:
            p.expect(pexpect.EOF)

        except pexpect.TIMEOUT:
            feedback += 'not ok EXPECTED END OF EXECUTION\n'
            feedback += '---at {!r}\n'.format(quote)
            feedback += 'FAILED!\n'
            result = False

        else:
            feedback += 'exit code {}\n'.format(p.exitstatus)
            feedback += 'SUCCEED!\n'
            result = True

    return result, feedback

def run_scenario(executable_path, scenario_path):
    scenario = parse_scenario_file(scenario_path)
    result, feedback = play_scenario(scenario, executable_path)

    return result, feedback