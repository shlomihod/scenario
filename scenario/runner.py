# -*- coding: utf-8 -*-

from scenario.parser import parse_scenario_json
from scenario.player import play_scenario


def run_scenario(executable_path, scenario_path,
                 verbosity=None, timeout=None,
                 executable_extra_args=None):

    scenario = parse_scenario_json(scenario_path)

    if verbosity is not None:
        scenario['verbosity'] = verbosity

    if timeout is not None:
        scenario['timeout'] = timeout

    feedback = play_scenario(scenario, executable_path,
                             executable_extra_args)

    return feedback
