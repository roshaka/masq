from src.masq_constant import *

class MasqWarning(Warning):
    pass

class MasqKeywordArgumentConflict(MasqWarning):
    pass

class MasqLengthWarning(MasqWarning):
    pass

class NonStringWarning(MasqWarning):
    pass

 
