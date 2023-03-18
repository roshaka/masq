from masq_constant import *

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

def ERR_01():
    'masq_length must be an integer.'

def ERR_02():
    return 'masq_length must be -1 or greater.'

def ERR_03(masq_string):
    return f'masq_string "{masq_string}" must be a string'

def ERR_04(masq_string):
    return f'masq_string "{masq_string}" must have a length <= {MAX_MASQ_LENGTH}'

def ERR_05(masq_char):
    return f'masq_char "{masq_char}" must be a str of length 1 or one of the following special strings:\n{masq_char_specials()}'

def ERR_06(func_name):
    return f'{func_name} does not return a dictionary or list of dictionaries and cannot be decorated with @masq'