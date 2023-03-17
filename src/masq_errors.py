
class MasqError(Exception):
    pass

class MasqKeyError(MasqError):
    pass

class MasqLengthError(MasqError):
    pass

class MasqStringError(MasqError):
    pass

class FunctionReturnTypeError(MasqError):
    pass