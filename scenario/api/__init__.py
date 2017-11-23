import json
import copy

import jsonschema

from scenario.player.feedback_exceptions import TimeoutFeedbackError, \
    OverflowFeedbackError
from scenario.utils import get_result_dict, get_feedback_dict
from scenario.consts import FEEDBACK_JSON_SCHEMA


def _get_feedback_json(scenario, feedback_exception):
    feedback = copy.deepcopy(scenario)
    feedback['log'] = {'quotes': [], 'text': ''}
    feedback['result'] = get_result_dict(False)
    feedback['feedback'] = get_feedback_dict(feedback_exception())
    feedback['exit_code'] = None
    feedback['signal_code'] = None

    jsonschema.validate(feedback, FEEDBACK_JSON_SCHEMA)
    return json.dumps(feedback, indent=2, sort_keys=True)


def get_timeout_feedback_json(scenario):
    return _get_feedback_json(scenario, TimeoutFeedbackError)


def get_overflow_feedback_json(scenario):
    return _get_feedback_json(scenario, OverflowFeedbackError)
