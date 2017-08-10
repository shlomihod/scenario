# -*- coding: utf-8 -*-

import os

import json
import jsonschema

from scenario.consts import SCENARIO_JSON_SCHEMA

from scenario.parser.exceptions import ParserJSONLoadingError, \
                                       ParserJSONValidationError

def parse_scenario_json(scenario_path):
    with open(scenario_path) as f:
        try:
            scenario = json.load(f)
        except ValueError as e:
            raise ParserJSONLoadingError(e)

    try:
        jsonschema.validate(scenario, SCENARIO_JSON_SCHEMA)
    except jsonschema.ValidationError as e:
        raise ParserJSONValidationError(e)

    return scenario
