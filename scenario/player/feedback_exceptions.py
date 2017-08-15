# -*- coding: utf-8 -*-

'''
========================
Feedback Exception Logic
========================

Scenario "consume" all the Input in the Executable, then:

+-----------------------------------------------------------+
| Executable          | Scenario    | Feedback              |
+ ====================+=============+=======================+
| EOF                 | More Input  | ShouldInputBeforeEOF  |
+---------------------+-------------+-----------------------+
| EOF                 | More Output | ShouldOutputBeforeEOF |
+---------------------+-------------+-----------------------+
| Input or            | EOF         | ShouldEOF             |
| Not Exiting         |             |                       |
+---------------------+-------------+-----------------------+
| Input or            | More Output | ShouldOutput          |
| Not Exiting         |             |                       |
+---------------------+-------------+-----------------------+
| Signal              |             | MemoryFeedbackError   |
+---------------------+-------------+-----------------------+
'''


class FeedbackException(Exception):
    def __init__(self, msg, quote=None):
        Exception.__init__(self)
        self.quote = quote
        self.feedback = msg.format(**quote)


class ShouldOutput(FeedbackException):
    '''
    The output is not just before EOF
    '''

    msg = u'הפלט {name} {value} לא הופיע או הופיע במקום הלא מתאים.'

    def __init__(self, quote):
        FeedbackException.__init__(self, ShouldOutput.msg, quote)


class ShouldEOF(FeedbackException):
    msg = u'ריצת התכנית אמורה הייתה להסתיים לאחר הקלטים והפלטים שנבדקו, אך התכנית עדיין רצה.' + u'\n' + \
          u'אולי יש לולאה אינסופית בקוד? אולי יש getchar מיותר בסוף ה-main?'

    def __init__(self, quote):
        FeedbackException.__init__(self, ShouldEOF.msg, quote)


class ShouldOutputBeforeEOF(FeedbackException):
    msg = u'ריצת התכנית הסתיימה, אך הפלט {name} {value} לא הופיע או הופיע במקום הלא מתאים לפי כן.'

    def __init__(self, quote):
        FeedbackException.__init__(self, ShouldOutputBeforeEOF.msg, quote)


class SholdNoOutputBeforeInput(FeedbackException):
    '''
    only in `flow = False`
    '''

    msg = u'התכנית לא הייתה אמורה להדפיס פלט לפני קבלת הקלט {name} {value}'

    def __init__(self, quote):
        FeedbackException.__init__(self, SholdNoOutputBeforeInput.msg, quote)


class ShouldInputBeforeEOF(FeedbackException):
    msg = u'ריצת התכנית הסתיימה, אך התכנית אמורה הייתה לקלוט את הקלט {name} {value}.'

    def __init__(self, quote):
        FeedbackException.__init__(self, ShouldInputBeforeEOF.msg, quote)


class MemoryFeedbackError(FeedbackException):
    msg = u'התרחשה שגיאת זיכרון'

    def __init__(self):
        FeedbackException.__init__(self, MemoryFeedbackError.msg, {})
