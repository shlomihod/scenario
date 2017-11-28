import json

import jsonschema

from scenario.parser import parse_scenario_json
from scenario.player.feedback_exceptions import TimeoutFeedbackError, \
    OverflowFeedbackError
from scenario.utils import get_result_dict, get_feedback_dict
from scenario.consts import FEEDBACK_JSON_SCHEMA


def _get_feedback_json(scenario_path, feedback_exception):
    feedback = parse_scenario_json(scenario_path)
    feedback['log'] = {'quotes': [], 'text': ''}
    feedback['result'] = get_result_dict(False)
    feedback['feedback'] = get_feedback_dict(feedback_exception())
    feedback['exit_code'] = None
    feedback['signal_code'] = None

    jsonschema.validate(feedback, FEEDBACK_JSON_SCHEMA)
    return json.dumps(feedback, indent=2, sort_keys=True)


def get_timeout_feedback_json(scenario_path):
    return _get_feedback_json(scenario_path, TimeoutFeedbackError)


def get_overflow_feedback_json(scenario_path):
    return _get_feedback_json(scenario_path, OverflowFeedbackError)
