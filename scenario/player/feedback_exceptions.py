# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
========================
Feedback Exception Logic
========================

Scenario "consume" all the Input in the Executable, then:

+-----------------------------------------------------------+----------+
| Executable          | Scenario    | Feedback              | Invoke   |
+ ====================+=============+=======================+==========+
| EOF                 | More Input  | ShouldInputBeforeEOF  | Internal |
+---------------------+-------------+-----------------------+----------+
| EOF                 | More Output | ShouldOutputBeforeEOF | Internal |
+---------------------+-------------+-----------------------+----------+
| Input or            | EOF         | ShouldEOF             | Internal |
| Not Exiting         |             |                       |          |
+---------------------+-------------+-----------------------+----------+
| Input or            | More Output | ShouldOutput          | Internal |
| Not Exiting         |             |                       |          |
+---------------------+-------------+-----------------------+----------+
| Signal              |             | MemoryFeedbackError   | Internal |
+---------------------+-------------+-----------------------+----------+
| Timeout             |             | TimeoutFeedbackError  | External |
+---------------------+-------------+-----------------------+----------+
| Overflow            |             | OverflowFeedbackError | External |
+---------------------+-------------+-----------------------+----------+
'''


class FeedbackException(Exception):
    def __init__(self, msg, quote=None):
        Exception.__init__(self)
        self.quote = quote
        self.feedback = msg.format(**quote)


class InternalFeedbackException(FeedbackException):
    def __init__(self, msg, quote=None):
        FeedbackException.__init__(self, msg, quote)


class ShouldOutput(InternalFeedbackException):
    '''
    The output is not just before EOF
    '''

    msg = 'הפלט {name} ({value}) לא הופיע או הופיע במקום הלא מתאים.'

    def __init__(self, quote):
        InternalFeedbackException.__init__(self, ShouldOutput.msg, quote)


class ShouldEOF(InternalFeedbackException):
    msg = 'ריצת התכנית אמורה הייתה להסתיים לאחר הקלטים והפלטים שנבדקו, אך התכנית עדיין רצה.' + '\n' + \
          'אולי התכנית מחכה לקלט נוסף שהיא לא הייתה אמורה לקלוט? אולי יש לולאה אינסופית בקוד? אולי יש getchar מיותר בסוף ה-main?'

    def __init__(self, quote):
        InternalFeedbackException.__init__(self, ShouldEOF.msg, quote)


class ShouldOutputBeforeEOF(InternalFeedbackException):
    msg = 'ריצת התכנית הסתיימה, אך הפלט {name} ({value}) לא הופיע או הופיע במקום הלא מתאים לפי כן.'

    def __init__(self, quote):
        InternalFeedbackException.__init__(self, ShouldOutputBeforeEOF.msg, quote)


class SholdNoOutputBeforeInput(InternalFeedbackException):
    '''
    only in `flow = False`
    '''

    msg = 'התכנית לא הייתה אמורה להדפיס פלט לפני קבלת הקלט {name} ({value})'

    def __init__(self, quote):
        InternalFeedbackException.__init__(self, SholdNoOutputBeforeInput.msg, quote)


class ShouldInputBeforeEOF(InternalFeedbackException):
    msg = 'ריצת התכנית הסתיימה, אך התכנית אמורה הייתה לקלוט את הקלט {name} ({value}).'

    def __init__(self, quote):
        InternalFeedbackException.__init__(self, ShouldInputBeforeEOF.msg, quote)


class MemoryFeedbackError(InternalFeedbackException):
    msg = 'התרחשה שגיאת זיכרון.'

    def __init__(self):
        InternalFeedbackException.__init__(self, MemoryFeedbackError.msg, {})


class ExternalFeedbackException(FeedbackException):
    def __init__(self, msg, quote=None):
        FeedbackException.__init__(self, msg, quote)


class TimeoutFeedbackError(ExternalFeedbackException):
    msg = 'התכנית רצה יותר מדי זמן. אולי יש לולאה אינסופית בקוד?'

    def __init__(self):
        ExternalFeedbackException.__init__(self, TimeoutFeedbackError.msg, {})


class OverflowFeedbackError(ExternalFeedbackException):
    msg = 'התכנית השתמשה ביותר מדי זיכרון. אולי התכנית מדפיסה יותר מדי פלט? אולי יש לולאה אינסופית בקוד?'

    def __init__(self):
        ExternalFeedbackException.__init__(self, OverflowFeedbackError.msg, {})
