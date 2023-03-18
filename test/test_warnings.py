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
        
    # TODO masq_length max length or =-1 on non string value

def test_masq_raises_warning_for_max_length_minus_one_on_non_string_value():
    input= {
    'name': 'Jane Smith',
    'email': 'jane@coolmail.com',
    'telephones': {
        'mobile': '07999 987654'
        },
    'status': 6
    }
    with pytest.warns(NonStringWarning):
        @masq('status', masq_length=-1)
        def foo():
            return input
        
        output=foo()
        assert output == {
            'name': 'Jane Smith',
            'email': 'jane@coolmail.com',
            'telephones': {
                'mobile': '07999 987654'
            },
            'status': '***'
        }

    