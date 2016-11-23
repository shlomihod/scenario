import os

from _consts import ACTORS, FILE_COMMANDS, VERBOSITY

def parse_scenario_line(scenario_line):
    parts = tuple(scenario_line.split(': ', 1))

    assert len(parts) == 2, 'Each line should be in the format of <actor>: <quote>'
    assert parts[0] in ACTORS, '{!r} is not recognized actor (Only {})' \
                                .format(parts[0], ACTORS)

    return parts

def parse_file_quote(file_quote, scenario_path, executable_path):
    '''
    TODO: better names
    quote[0] - command
    quote[1] - exec env file path
    quote[2] - snr env file path
    quote[3] - exec full file path
    quote[4] - snr full file path
    '''

    parts = file_quote.split()
    assert len(parts) == 3, 'Each file quote should be in the format of <command> <exec env file path> <snr env file path>'
    assert parts[0] in FILE_COMMANDS, '{!r} is not recognized file command (Only {})' \
                                .format(parts[0], FILE_COMMANDS)

    exec_env_file_path = os.path.join(os.path.dirname(executable_path), parts[1])
    snr_env_file_path = os.path.join(os.path.dirname(scenario_path), parts[2])

    parts = tuple(parts + [exec_env_file_path, snr_env_file_path])
    return parts


def parse_scenario_file(scenario_path, executable_path):
    with open(scenario_path, 'r') as f:
        lines = f.read().splitlines()

    name = None
    args = None
    verbosity = None

    pre_dialog = []
    dialog = []

    assert len(lines) != 0, 'Scenario file cannot be empty'

    parsed_line = parse_scenario_line(lines[0])
    assert parsed_line[0] == 'N', 'Frist line sholud be Name'
    assert parsed_line[1].strip() != '', 'Cannot be empty name'
    name = parsed_line[1].strip()

    try:
        for i, line in enumerate(lines[1:]):
            if line:
                parsed_line = parse_scenario_line(line)

                if parsed_line[0] == 'R':
                    continue
                
                elif parsed_line[0] == 'A':
                    assert args is None, 'Cannot be more than one A actor'
                    assert dialog == [], 'Cannot be I or O actors before A actor'
                    args = parsed_line[1]
                
                elif parsed_line[0] == 'V':
                    assert verbosity is None, 'Cannot be more than one V actor'
                    if parsed_line[1] in VERBOSITY.keys():
                        verbosity = parsed_line[1]
                    elif parsed_line[1] in map(str, VERBOSITY.values()):
                        verbosity = VERBOSITY.keys()[
                                        map(str, VERBOSITY.values()).index(parsed_line[1])
                                    ]
                    else:
                        raise AssertionError('V actor is {!r} but it must be only one of {!s} or one of {!s}'.
                                            format(parsed_line[1], VERBOSITY.keys(), VERBOSITY.values())) 

                elif parsed_line[0] == 'F':
                    quote = (parsed_line[0], parse_file_quote(parsed_line[1], scenario_path, executable_path))
                    if args is None:
                        pre_dialog.append(quote)
                    else:
                        dialog.append(quote)
                
                elif parsed_line[0] == 'N':
                    raise AssertionError('Cannot be more than one N actor')
            
                elif parsed_line[0] in ['I', 'O']:
                    dialog.append(parsed_line)


    except AssertionError as e:
        raise RuntimeError('Error in scenario file at line {}: {}' \
                            .format(i+2, e))

    return {'name': name, 'args': args, 'dialog': dialog, 'pre_dialog': pre_dialog, 'verbosity': verbosity}