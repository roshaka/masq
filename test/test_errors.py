from src.masq import masq
from src.masq_errors import *
from test_dummies.dummies import dummy_dict
import pytest

def test_invalid_target_key_raises_MasqKeyError():
    @masq('banana')
    def foo():
        return dummy_dict()

    with pytest.raises(MasqKeyError):
        foo()

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

def test_non_int_type_masq_length_raises_MasqLengthError():
    with pytest.raises(FunctionReturnTypeError) as e:
        @masq('name')
        def foo():
            return "not a dict"
        foo()

    assert str(e.value) == "foo does not return a dictionary and cannot be decorated with @masq"

