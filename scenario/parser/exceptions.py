class ParserError(Exception):
    pass


class ParserJSONLoadingError(ParserError):
    def __init__(self, json_decode_error):
        self.json_decode_error = json_decode_error
        self.msg = 'Failed Loading Scenario JSON\n' + \
                   str(json_decode_error)


class ParserJSONValidationError(ParserError):
    def __init__(self, validation_error):
        self.validation_error = validation_error
        self.msg = validation_error.message
