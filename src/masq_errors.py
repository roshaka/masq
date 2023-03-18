from src.masq_constant import *

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
