from src.masq import masq
from src.masq_errors import *
from test_dummies.dummies import dummy_dict
import pytest
from src.masq_constant import *

def test_invalid_target_key_raises_MasqKeyError():
    @masq('banana')
    def foo():
        return dummy_dict()

    with pytest.raises(MasqKeyError):
        foo()

def test_invalid_masq_string_raises_MasqStringError():

    with pytest.raises(MasqStringError) as e:
        @masq('name', masq_string=[])
        def foo():
            return dummy_dict()

    assert str(e.value) == 'masq_string "[]" must be a string'

def test_masq_string_with_length_greater_than_max_masq_length_raises_MasqStringError():

    with pytest.raises(MasqStringError) as e:
        input_masq_string ='this is a really long string and will raise a MasqStringError'
        @masq('name', masq_string=input_masq_string)
        def foo():
            return dummy_dict()

    assert str(e.value) == f'masq_string "{input_masq_string}" must have a length <= {MAX_MASQ_LENGTH}'

def test_invalid_masq_length_value_raises_MasqLengthError():
    with pytest.raises(MasqLengthError):
        @masq(masq_length=-4)
        def foo():
            return dummy_dict()
     
def test_non_int_type_masq_length_raises_MasqLengthError():
    with pytest.raises(MasqLengthError):
        @masq(masq_length='whoops')
        def foo():
            return dummy_dict()

def test_decorating_a_function_that_does_not_return_dict_with_masq_raises_FunctionReturnTypeError():
    with pytest.raises(FunctionReturnTypeError) as e:
        @masq('name')
        def foo():
            return "not a dict"
        foo()

    assert str(e.value) == "foo does not return a dictionary or list of dictionaries and cannot be decorated with @masq"
def test_decorating_a_function_that_does_not_return_list_of_dicts_with_masqs_raises_FunctionReturnTypeError():
    with pytest.raises(FunctionReturnTypeError) as e:
        @masq('name')
        def foo():
            return "not a list of dicts"
        foo()

    assert str(e.value) == "foo does not return a dictionary or list of dictionaries and cannot be decorated with @masq"

def test_validate_masq_char_raises_MasqCharError_for_non_string_type_input():
    with pytest.raises(MasqCharError) as e:
        @masq('name', masq_char=[])
        def foo():
            return dummy_dict
        foo()

    assert str(e.value) == 'masq_char "[]" must be type string'

def test_validate_masq_char_raises_MasqCharError_if_str_length_greater_than_1_and_not_special():
    with pytest.raises(MasqCharError) as e:
        @masq('name', masq_char='no')
        def foo():
            return dummy_dict

    assert str(e.value) == f'masq_char "no" must be a str of length 1 or one of the following special strings:\n{masq_char_specials()}'
