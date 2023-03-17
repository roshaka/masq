from src.masq import masq, masqs
from unittest.mock import patch
from test_dummies.dummies import *
import pytest

# TODO
# def test_masq_decorator_returns_original_dictionary_if_no_target_keys():
#     '''Tests that the original dictionary object is returned if no target_keys sepecified in the masq'''
#     input =  dummy_dict()

#     @masq()
#     def foo():
#         return input
    
#     output = foo()
#     assert input == output

def test_masq_decorator_masks_single_target_key():
    '''Tests that masq decorator with single target_key masks target dictionary key'''
    @masq('name')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()
    assert masqed_dict == {
        'name': '***',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masq_decorator_masks_single_nested_target_key():
    '''Tests that masq decorator with single target_key masks target dictionary key'''
    @masq('telephones.mobile')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()
    assert masqed_dict == {
        'name': 'Jane Smith',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '***'
        },
        'status': 'excellent'
    }
    
def test_masq_decorator_masks_multiple_target_keys():
    '''Tests that masq decorator with multiple target_keys masks all target dictionary keys'''
    @masq('name','email')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()
    assert masqed_dict == {
        'name': '***',
        'email': '***',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masq_char_keyword_param():
    '''Tests that the masked value is created by the masq_char'''
    @masq('name', masq_char='?')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()
    assert masqed_dict == {
        'name': '???',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masq_length_keyword_param():
    '''Tests that the masked value is created by the masq_char'''
    @masq('name', masq_length=7)
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()
    assert masqed_dict == {
        'name': '*******',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masq_length_maintains_length_of_original_key_if_minus_1():
    '''Tests that the masked value is created by the masq_char'''
    @masq('name', masq_length=-1)
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()

    assert masqed_dict == {
        'name': '**********',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

@patch('src.masq._get_random_grawlix_char', return_value ='#')
def test_masq_char_generates_grawlix_if_equals_grawlix(func):
    '''Tests masq_char="grawlix" returns random grawlix char'''
    @masq('name', masq_char='grawlix')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()

    assert masqed_dict == {
        'name': '###',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

@patch('src.masq._get_random_int_char', return_value ='4')
def test_masq_char_generates_random_ints_if_equals_numerics(func):
    '''Tests masq_char="numerics" returns random int char'''
    @masq('name', masq_char='numerics')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()

    assert masqed_dict == {
        'name': '444',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

@patch('src.masq._get_random_alpha_char', return_value ='X')
def test_masq_char_generates_random_ints_if_equals_numerics(func):
    '''Tests masq_char="alphas" returns random alpha char'''
    @masq('name', masq_char='alphas')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()

    assert masqed_dict == {
        'name': 'XXX',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_mask_string_overwrites_other_params_and_sets_value_equal_to_mask_string():
    @masq('name', 'email', masq_string='REDACTED')
    def foo():
        return dummy_dict()
    
    masqed_dict = foo()

    assert masqed_dict == {
        'name': 'REDACTED',
        'email': 'REDACTED',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masq_max_length_limits_masq():
    
    with pytest.warns(Warning):
        @masq('name', masq_length=100 )
        def foo():
            return dummy_dict()
    
    masqed_dict = foo()

    assert masqed_dict == {
        'name': '********************************',
        'email': 'jane@coolmail.com',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
    }

def test_masqs_decorator_performs_masq_on_list_of_dictionaries():
    '''Tests that all dicts in a list are masqed.'''
    @masqs('email')
    def foo():
        return dummy_dicts_list()
    
    masqed_dicts_list = foo()

    assert masqed_dicts_list == [
        {
        'name': 'Jane Smith',
        'email': '***',
        'telephones': {
            'mobile': '07999 987654'
        },
        'status': 'excellent'
        },
        {
        'name': 'David Jones',
        'email': '***',
        'telephones': {
            'mobile': '07787 123456'
        },
        'status': 'poor'
        }
    ]