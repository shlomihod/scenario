from collections import OrderedDict

ACTORS = list('NMRAIOVF')

FILE_COMMANDS = ['copy', 'compare']

MODES = ['STRICT', 'NONSTRICT', 'FLOW']

STRICTNESS_DEFUALT = True

FLOW_DEFAULT = False

VERBOSITY = OrderedDict(
            [ ('RETURN_CODE', 0),
              ('RESULT'     , 1),
              ('WARNING'    , 2),
              ('ERROR'      , 3),
              ('EXECUTION'  , 4),
              ('DEBUG'      , 5),
])    

VERBOSITY_DEFAULT = VERBOSITY['RESULT']

TIMEOUT_DEFAULT = 1
