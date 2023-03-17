from src.masq import masq
from test_dummies.dummies import dummy_dict
from src.masq_warnings import *
import pytest

def test_conflicting_masq_decorator_params_raise_warning():
    @masq('name', 'email', masq_string='REDACTED', masq_char='s')
    def foo():
        return dummy_dict()

    with pytest.warns(MasqKeywordArgumentConflict):
        foo()

def test_masq_length_greater_than_32_raises_MasqLengthWarning():
    with pytest.warns(MasqLengthWarning):
        @masq('name', masq_length=100)
        def foo():
            return dummy_dict()