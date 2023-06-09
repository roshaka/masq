'''Errors raised by the @masq decorator.'''
class MasqError(Exception):
    pass

class MasqKeyError(MasqError):
    pass

class MasqCharError(MasqError):
    pass

class MasqLengthError(MasqError):
    pass

class MasqStringError(MasqError):
    pass

class FunctionReturnTypeError(MasqError):
    pass

class InvalidMasqArgument(MasqError):
    pass

class InvalidMasqKeywordError(MasqError):
    pass
