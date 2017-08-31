# -*- coding: utf-8 -*-

from scenario.consts import RESULT_TEXT, QUOTE_TYPE_HE_TEXT


def xstr(s):
    if not isinstance(s, basestring):
        return ''
    return str(s)


def get_cleaned_before(p, strictness):
    if isinstance(p.before, str):

        if strictness:

            before_lines = p.before.split('\r\n')
            if not any([set(l) - set(' ') for l in before_lines[:-1]]):
                return before_lines[-1]
            else:
                return p.before.strip('\r\n')

        else:
            return p.before.strip(' \r\n')


def get_cleaned_after(p, strictness):
    if isinstance(p.after, str):

        if strictness:

            # In STRICT mode, spaces in the end of the line are ignored
            after_lines = p.after.split('\r\n')
            if (after_lines and
                    not any([set(l) - set(' ') for l in after_lines[1:]])):
                return after_lines[0].strip(' \r\n')
            else:
                return p.after.strip('\r\n')

        else:
            return p.after.strip(' \r\n')


def get_result_dict(result_bool):
    assert isinstance(result_bool, bool)

    return {'bool': result_bool,
            'text': RESULT_TEXT[result_bool]
            }


def get_feedback_dict(e):
    assert isinstance(e, Exception) or e is None

    if e is None:
        return {'type': None, 'text': None}
    else:
        return {'type': type(e).__name__,
                'text': e.feedback
                }


def get_quote_type_dict(quote_type):
    assert isinstance(quote_type, basestring)

    return {'en': quote_type,
            'he': QUOTE_TYPE_HE_TEXT[quote_type]
            }


def build_feedback_text(feedback):
    text = ''

    text += str(feedback['result']['bool'])
    text += '\n'
    text += feedback['id']

    text += '\n====\n'

    if not feedback['result']['bool']:
        text += feedback['feedback']['type']
        text += '\n====\n'

    text += feedback['log']['text']

    return text
