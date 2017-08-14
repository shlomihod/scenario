# -*- coding: utf-8 -*-

from scenario.consts import TIMEOUT_DEFAULT

from scenario.parser import parse_scenario_json
from scenario.player import play_scenario


def run_scenario(executable_path, scenario_path,
                 verbosity=None, timeout=TIMEOUT_DEFAULT,
                 executable_extra_args=None):

    scenario = parse_scenario_json(scenario_path)

    if verbosity is not None:
        scenario['verbosity'] = verbosity

    feedback = play_scenario(scenario, executable_path,
                             timeout, executable_extra_args)

    return feedback
