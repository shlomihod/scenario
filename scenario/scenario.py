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
    executable_path_with_args = executable_path + ' '+ scenario['args']
    p = pexpect.spawn(executable_path_with_args, timeout=TIMEOUT)

    try:
        for index, (actor, qoute) in enumerate(scenario['dialog']):
            if actor == 'O':
                match_index = p.expect_exact(qoute)
                print p.match

            elif actor == 'I':
                p.sendline(qoute)


        p.expect(pexpect.EOF)

    except pexpect.EOF:
        print 'EOF'

    except pexpect.TIMEOUT:
        print 'TIMEOUT'

    p.close()
    print p.exitstatus

def run_scenario(executable_path, scenario_path):
    scenario = parse_scenario_file(scenario_path)
    feedback = play_scenario(scenario, executable_path)