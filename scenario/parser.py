import os

from scenario.consts import ACTORS, FILE_COMMANDS, FILE_COMMANDS_PARAMS_2, FILE_COMMANDS_PARAMS_4, \
                            VERBOSITY, MODES, STRICTNESS_DEFUALT, FLOW_DEFAULT

def parse_scenario_line(scenario_line):
    parts = tuple(scenario_line.split(': ', 1))

    assert len(parts) == 2, 'Each line should be in the format of <actor>: <quote>'
    assert parts[0] in ACTORS, '{!r} is not recognized actor (Only {})' \
                                .format(parts[0], ACTORS)

    return parts

def parse_file_quote(file_quote, scenario_path, executable_path):
    '''
    quote[0] - command
    
    2:
    quote[1] - exec env file path
    quote[2] - exec full file path

    4:
    quote[1] - exec env file path
    quote[2] - snr env file path
    quote[3] - exec full file path
    quote[4] - snr full file path
    '''

    parts = file_quote.split()
    assert len(parts), 'File quote cannot be empty'
    assert parts[0] in FILE_COMMANDS, '{!r} is not recognized file command (Only {})' \
                                .format(parts[0], FILE_COMMANDS)
    
    if parts[0] in FILE_COMMANDS_PARAMS_2:
        assert len(parts) == 2, 'Each file quote should be in the format of <command> <exec env file path>'

        exec_env_file_path = os.path.join(os.path.dirname(executable_path), parts[1])

        parts = tuple(parts + [exec_env_file_path])

    elif parts[0] in FILE_COMMANDS_PARAMS_4:
        assert len(parts) == 3, 'Each file quote should be in the format of <command> <exec env file path> <snr env file path>'
   
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
    mode_flags = None
    strictness = STRICTNESS_DEFUALT
    flow = FLOW_DEFAULT

    pre_dialog = []
    dialog = []

    assert len(lines) != 0, 'Scenario file cannot be empty'

    parsed_line = parse_scenario_line(lines[0])
    assert parsed_line[0] == 'N', 'Frist line sholud be Name'
    assert parsed_line[1].strip() != '', 'Cannot be empty name'
    name = parsed_line[1].strip()

    try:
        for i, line in enumerate(lines[1:]):
            if line.strip():
                parsed_line = parse_scenario_line(line)

                if parsed_line[0] == 'R':
                    continue
                
                elif parsed_line[0] == 'A':
                    assert args is None, 'Cannot be more than one A actor'
                    assert dialog == [], 'Cannot be I or O actors before A actor'
                    args = parsed_line[1]

                elif parsed_line[0] == 'M':
                    assert mode_flags is None, 'Cannot be more than one M actor'
                    mode_flags = parsed_line[1].split()
                    if not all([f in MODES for f in mode_flags]):
                        raise AssertionError('M actor is {!r} but it all of the flags must be only one of {!s}'.
                                            format(parsed_line[1], MODES))
                    assert len(mode_flags) <= 2, 'Only one or two Mode flag is allowed, there are {!s}'.format(len(mode_flags))
                    if 'STRICT' in mode_flags:
                        strictness = True
                    elif 'NONSTRICT' in mode_flags:
                        strictness = False

                    if 'FLOW' in mode_flags:
                        flow = True

                elif parsed_line[0] == 'V':
                    assert verbosity is None, 'Cannot be more than one V actor'
                    rstriped_quote = parsed_line[1].rstrip()
                    if rstriped_quote in VERBOSITY.keys():
                        verbosity = rstriped_quote
                    elif rstriped_quote in map(str, VERBOSITY.values()):
                        verbosity = VERBOSITY.keys()[
                                        map(str, VERBOSITY.values()).index(rstriped_quote)
                                    ]
                    else:
                        raise AssertionError('V actor is {!r} but it must be only one of {!s} or one of {!s}'.
                                            format(parsed_line[1], VERBOSITY.keys(), VERBOSITY.values())) 

                elif parsed_line[0] == 'F':
                    dialog_line = (parsed_line[0], parse_file_quote(parsed_line[1], scenario_path, executable_path))
                    if args is None:
                        pre_dialog.append(dialog_line)
                    else:
                        dialog.append(dialog_line)
                
                elif parsed_line[0] == 'N':
                    raise AssertionError('Cannot be more than one N actor')
            
                elif parsed_line[0] in ['O', 'I']:
                    dialog.append(parsed_line)


    except AssertionError as e:
        raise RuntimeError('Error in scenario file at line {}: {}' \
                            .format(i+2, e))

    return {
            'name': name,
            'args': args,
            'dialog': dialog,
            'pre_dialog': pre_dialog,
            'verbosity': verbosity,
            'strictness': strictness,
            'flow': flow
           }
