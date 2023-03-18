from masq_constant import *

class MasqWarning(Warning):
    pass

class MasqKeywordArgumentConflict(MasqWarning):
    pass

class MasqLengthWarning(MasqWarning):
    pass

class NonStringWarning(MasqWarning):
    pass

WARN_01 = f'masq_length must be less than or equal to {MAX_MASQ_LENGTH}'
