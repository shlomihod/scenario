# -*- coding: utf-8 -*-

import os

import json
import jsonschema

from consts import SCENARIO_JSON_SCHEMA

def parse_scenario_file(scenario_path, executable_path):
    with open(scenario_path) as f:
        scenario = json.load(f)

    jsonschema.validate(scenario, SCENARIO_JSON_SCHEMA)

    return scenario
