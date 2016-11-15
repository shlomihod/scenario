from collections import OrderedDict

ACTORS = list('NRAIOV')

VERBOSITY = OrderedDict(
            [ ('RETURN_CODE', 0),
              ('RESULT'     , 1),
              ('ERROR'      , 2),
              ('EXECUTION'  , 3),
              ('DEBUG'      , 4),
])    

VERBOSITY_DEFAULT = VERBOSITY['RESULT']

TIMEOUT_DEFAULT = 1