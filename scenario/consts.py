# -*- coding: utf-8 -*-

from collections import OrderedDict
import json
import pkg_resources

SCENARIO_JSON_SCHEMA_PATH = 'schema/scenario.json'
SCENARIO_JSON_SCHEMA = json.load(pkg_resources.resource_stream('scenario', SCENARIO_JSON_SCHEMA_PATH))

FEEDBACK_JSON_SCHEMA_PATH = 'schema/feedback.json'
FEEDBACK_JSON_SCHEMA = json.load(pkg_resources.resource_stream('scenario', FEEDBACK_JSON_SCHEMA_PATH))

VERBOSITY = OrderedDict(
            [ ('RETURN_CODE', 0),
              ('RESULT'    , 1),
              ('WARNING'   , 2),
              ('ERROR'     , 3),
              ('EXECUTION' , 4),
              ('DEBUG'     , 5),
])

TIMEOUT_DEFAULT = 1

OUTPUT_FORMATS = ['json', 'text']
OUTPUT_FORMATS_DEFAULT = 'text'

RESULT_TEXT = { False : u'אי-הצלחה',
                True  : u'הצלחה'
               }

QUOTE_TYPE_HE_TEXT = { 'printing' : u'הדפסה',
              'output'   : u'פלט',
              'input'    : u'קלט'
            }

# https://people.cs.pitt.edu/~alanjawi/cs449/code/shell/UnixSignals.htm
SIGNALS = {
 1: ('SIGHUP', 'Hangup'),
 2: ('SIGINT', 'Interrupt'),
 3: ('SIGQUIT', 'Quit'),
 4: ('SIGILL', 'Illegal Instruction'),
 5: ('SIGTRAP', 'Trace/Breakpoint Trap'),
 6: ('SIGABRT', 'Abort'),
 7: ('SIGEMT', 'Emulation Trap'),
 8: ('SIGFPE', 'Arithmetic Exception'),
 9: ('SIGKILL', 'Killed'),
 10: ('SIGBUS', 'Bus Error'),
 11: ('SIGSEGV', 'Segmentation Fault'),
 12: ('SIGSYS', 'Bad System Call'),
 13: ('SIGPIPE', 'Broken Pipe'),
 14: ('SIGALRM', 'Alarm Clock'),
 15: ('SIGTERM', 'Terminated'),
 16: ('SIGUSR1', 'User Signal 1'),
 17: ('SIGUSR2', 'User Signal 2'),
 18: ('SIGCHLD', 'Child Status'),
 19: ('SIGPWR', 'Power Fail/Restart'),
 20: ('SIGWINCH', 'Window Size Change'),
 21: ('SIGURG', 'Urgent Socket Condition'),
 22: ('SIGPOLL', 'Socket I/O Possible'),
 23: ('SIGSTOP', 'Stopped (signal)'),
 24: ('SIGTSTP', 'Stopped (user)'),
 25: ('SIGCONT', 'Continued'),
 26: ('SIGTTIN', 'Stopped (tty input)'),
 27: ('SIGTTOU', 'Stopped (tty output)'),
 28: ('SIGVTALRM', 'Virtual Timer Expired'),
 29: ('SIGPROF', 'Profiling Timer Expired'),
 30: ('SIGXCPU', 'CPU time limit exceeded'),
 31: ('SIGXFSZ', 'File size limit exceeded'),
 32: ('SIGWAITING', 'All LWPs blocked'),
 33: ('SIGLWP', 'Virtual Interprocessor Interrupt for Threads Library'),
 34: ('SIGAIO', 'Asynchronous I/O')
 }
