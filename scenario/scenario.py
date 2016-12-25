from _consts import VERBOSITY, VERBOSITY_DEFAULT, TIMEOUT_DEFAULT

from parser import parse_scenario_file
from player import play_scenario

def run_scenario(executable_path, scenario_path, verbosity=None, timeout=TIMEOUT_DEFAULT, executable_extra_args=None):

    scenario = parse_scenario_file(scenario_path, executable_path)

    if verbosity is None:
        if scenario['verbosity'] is not None:
            verbosity = VERBOSITY[scenario['verbosity']]
        else:
            verbosity = VERBOSITY_DEFAULT

    result, feedback = play_scenario(scenario, executable_path, verbosity, timeout)

    return result, feedback