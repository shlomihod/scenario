from collections import OrderedDict

ACTORS = list('NRAIOVF')

FILE_COMMANDS = ['copy', 'compare']

VERBOSITY = OrderedDict(
            [ ('RETURN_CODE', 0),
              ('RESULT'     , 1),
              ('ERROR'      , 2),
              ('EXECUTION'  , 3),
              ('DEBUG'      , 4),
])    

VERBOSITY_DEFAULT = VERBOSITY['RESULT']

TIMEOUT_DEFAULT = 1