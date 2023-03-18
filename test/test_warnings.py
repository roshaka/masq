'''
Tests for warnings with @masq decorator.
'''
from src.masq import masq
from test_dummies.dummies import dummy_dict
from src.masq_warnings import NonStringWarning, MasqKeywordConflict, MasqLengthWarning
import pytest

def test_conflicting_masq_args_raise_warning():
    '''Tests for warning if conflicting masq args are used.'''
    @masq('name', 'email', masq_string='REDACTED', masq_char='s', emit_warnings=True)
    def foo():
        return dummy_dict()

    with pytest.warns(MasqKeywordConflict):
        foo()

def test_masq_length_greater_than_max_masq_length_raises_MasqLengthWarning():
    '''Tests max length of masq_string is limited to max_masq_length. '''
    with pytest.warns(MasqLengthWarning):
        @masq('name', masq_length=100, emit_warnings=True)
        def foo():
            return dummy_dict()

def test_masq_raises_warning_for_max_length_minus_one_on_non_string_value():
    '''Tests error is raised when trying to get masq_length from non-string value.'''
    input= {
    'name': 'Jane Smith',
    'email': 'jane@coolmail.com',
    'telephones': {
        'mobile': '07999 987654'
        },
    'status': 6
    }
    with pytest.warns(NonStringWarning):
        @masq('status', masq_length=-1, emit_warnings=True)
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

    