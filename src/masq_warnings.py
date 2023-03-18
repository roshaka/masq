'''Warnings raised by the @masq decorator.'''
class MasqWarning(Warning):
    pass

class MasqKeywordConflict(MasqWarning):
    pass

class MasqLengthWarning(MasqWarning):
    pass

class NonStringWarning(MasqWarning):
    pass

 
