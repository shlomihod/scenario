class FileContentIncorrect(Exception):
    pass

class ShouldEOF(Exception):
    pass

class ShouldOutputBeforeEOF(Exception):
    pass

class OutputBeforeInput(Exception):
    pass

class ShouldInputBeforeEOF(Exception):
    pass
