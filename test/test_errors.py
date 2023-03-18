'''
Tests for errors with @masq decorator.
'''
from src.masq import masq
from src.masq_errors import MasqKeyError, MasqStringError, MasqLengthError
from src.masq_errors import FunctionReturnTypeError, MasqCharError
from test_dummies.dummies import dummy_dict
import pytest

def test_invalid_target_key_raises_MasqKeyError():
    '''Tests invalid target_key raises MasqKeyError.'''
    @masq('banana')
    def foo():
        return dummy_dict()

    with pytest.raises(MasqKeyError):
        foo()

def test_invalid_masq_string_raises_MasqStringError():
    '''Tests invalid masq_string raises MasqStringError.'''
    with pytest.raises(MasqStringError):
        @masq('name', masq_string=[])
        def foo():
            return dummy_dict()

def test_masq_string_with_length_greater_than_max_masq_length_raises_MasqStringError():
    '''Tests masq_string with len> max_masq_length raises error.'''
    with pytest.raises(MasqStringError):
        input_masq_string ='this is a really long string and will raise MasqStringError'
        @masq('name', masq_string=input_masq_string)
        def foo():
            return dummy_dict()

def test_invalid_masq_length_value_raises_MasqLengthError():
    '''Negative masq_length raises MasqLengthError.'''
    with pytest.raises(MasqLengthError):
        @masq(masq_length=-4)
        def foo():
            return dummy_dict()
     
def test_non_int_type_masq_length_raises_MasqLengthError():
    '''Tests non int type for masq_length raises error.'''
    with pytest.raises(MasqLengthError):
        @masq(masq_length='whoops')
        def foo():
            return dummy_dict()

def test_masq_on_func_that_does_not_return_dict_or_dicts_list_raises_error():
    '''Tests masq on a func that does not return a dict or dicts list raises error.'''
    with pytest.raises(FunctionReturnTypeError):
        @masq('name')
        def foo():
            return 'not a dict'
        foo()

def test_validate_masq_char_raises_MasqCharError_for_non_string_type_input():
    '''Tests masq_char raises error if not equal to string.'''
    with pytest.raises(MasqCharError):
        @masq('name', masq_char=6)
        def foo():
            return dummy_dict
        foo()

def test_validate_masq_char_raises_MasqCharError_for_invalid_masq_char():
    '''Tests masq_char is single char or special string, else raises error.'''
    with pytest.raises(MasqCharError):
        @masq('name', masq_char='no')
        def foo():
            return dummy_dict
