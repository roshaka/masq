'''Constants used by the @masq decorator.'''
DEFAULT_MASQ_LENGTH=3
MAX_MASQ_LENGTH=32

MAX_CHAR_ALPHAS='alphas'
MAX_CHAR_NUMERICS='numerics'
MAX_CHAR_GRAWLIX='grawlix'

def masq_char_specials():
    return [
        MAX_CHAR_ALPHAS,
        MAX_CHAR_NUMERICS,
        MAX_CHAR_GRAWLIX
    ]
